# /// script
# requires-python = ">=3.10"
# dependencies = ["openrouter>=1.3.32", "python-dotenv>=1.0", "lameenc>=1.7"]
# ///
"""Read the narration aloud with a text-to-speech model on OpenRouter.

usage: uv run speak.py en|es [--model M] [--voice V] [--only cover,agenda] [--out DIR] [--force]
                            [--env-file PATH]

Reads <lang>.json (per slide, one segment per build step) and writes <out>/<NN>-<slide>-s<K>.mp3,
by default into audio/<lang>/. Audio is requested as PCM, which every TTS model offers, and
encoded to 48 kbps mono MP3 here. Files that already exist are skipped, so a rerun only pays for
what is missing. The key comes from OPENROUTER_API_KEY, or from the .env file named by
--env-file; it is never printed. The run ends with what it cost, from the account's credits.
"""
import argparse
import json
import os
import pathlib
import re
import sys

import lameenc
from dotenv import load_dotenv
from openrouter import OpenRouter

HERE = pathlib.Path(__file__).resolve().parent
STYLE = {
    'en': 'Read this as the narrator of a recorded conference talk: clear, calm and engaged, at an unhurried pace.',
    'es': 'Lee esto como la voz de una charla grabada: clara, tranquila y atenta, a un ritmo pausado, '
          'en español latinoamericano neutro.',
}


def to_mp3(pcm, rate):
    enc = lameenc.Encoder()
    enc.set_bit_rate(48)
    enc.set_in_sample_rate(rate)
    enc.set_channels(1)
    enc.set_quality(2)
    return enc.encode(pcm) + enc.flush()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('lang', choices=sorted(STYLE))
    ap.add_argument('--model', default='google/gemini-3.8-flash-tts')
    ap.add_argument('--voice', default='Charon')
    ap.add_argument('--instructions', help='style prompt (default: a narrator style per language; "" sends none)')
    ap.add_argument('--only', help='comma-separated slide ids')
    ap.add_argument('--out', type=pathlib.Path)
    ap.add_argument('--force', action='store_true', help='redo files that exist')
    ap.add_argument('--env-file', type=pathlib.Path)
    args = ap.parse_args()

    if args.env_file:
        load_dotenv(args.env_file)
    if not os.environ.get('OPENROUTER_API_KEY'):
        sys.exit('Set OPENROUTER_API_KEY, or pass --env-file with a .env that defines it.')
    narration = json.loads((HERE / f'{args.lang}.json').read_text(encoding='utf-8'))
    only = set(args.only.split(',')) if args.only else None
    out = args.out or HERE / 'audio' / args.lang
    out.mkdir(parents=True, exist_ok=True)
    instructions = STYLE[args.lang] if args.instructions is None else args.instructions or None

    with OpenRouter(api_key=os.environ['OPENROUTER_API_KEY'], timeout_ms=120_000) as client:
        spent_before = client.credits.get_credits().data.total_usage
        made = 0
        for n, (slide, segments) in enumerate(narration.items(), 1):
            if only and slide not in only:
                continue
            for k, text in enumerate(segments):
                path = out / f'{n:02d}-{slide}-s{k}.mp3'
                if path.exists() and not args.force:
                    continue
                res = client.tts.create_speech(input=text, model=args.model, voice=args.voice,
                                               instructions=instructions, response_format='pcm')
                try:
                    rate = re.search(r'rate=(\d+)', res.headers.get('content-type', ''))
                    path.write_bytes(to_mp3(res.read(), int(rate.group(1)) if rate else 24000))
                finally:
                    res.close()
                made += 1
                print(path.relative_to(out.parent), f'{path.stat().st_size // 1024} KB', res.headers.get('content-type'), flush=True)
        spent = client.credits.get_credits().data.total_usage - spent_before
    print(f'{made} files, ${spent:.4f} (credit usage can lag by a few seconds)')


if __name__ == '__main__':
    main()
