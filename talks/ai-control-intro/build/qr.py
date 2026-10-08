# /// script
# requires-python = ">=3.10"
# dependencies = ["segno"]
# ///
import segno, json
urls={'metr':'https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/',
      'openai':'https://openai.com/index/hugging-face-incident-and-the-road-ahead/',
      'dsewiki':'https://dsewiki.de'}
out={}
for k,u in urls.items():
    q=segno.make(u, error='m', boost_error=False)
    m=[[1 if c else 0 for c in row] for row in q.matrix]
    out[k]={'url':u,'version':q.version,'n':len(m),'matrix':m}
    print(k,q.version,len(m))
json.dump(out,open('qr.json','w'))
