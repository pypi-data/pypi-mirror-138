<h1 align="center">Wire</h1>
<p align="center"> Easy, fast, stable </p>
<img src="https://cdn.discordapp.com/attachments/857979752991031296/928221250520760330/wire1.png" align="right" style="margin-top: -50px;"/>
<br>
<br>
Wire is designed to provide the user with the greatest possible comfort when creating Rest APIs or entire websites.
Everything is simple and, above all, intuitively designed. No focus on superfluous configurations. Everything works, simply.

🔑 Key features

- intuitive, due to the clear design
- simple, due to the fast learning curve
- practical, through the great editor support
- minimalistic, no superfluous functions

#### What is Wire and what is not

Wire is not a HighSpeed framework. Wire is probably not ready for production. Wire is a spare time project of mine. Wire is self-contained. It doesn't need anything, except for an ASGI server. So it's like Starlette.
I would appreciate if you use Wire, try it and give me your feedback.

#### Participate in Wire

You are welcome to collaborate on Wire. However, you should maintain the codestyle, and also follow PEP 8 (the Python style guide).

#### Wire disadvantages

Wire is still deep in development, which is why some features are still missing. 

- Websockets

#### Examples

Here is the most basic example of wire

```py
from wire import Wire, Request

app = Wire()

@app.get("/home")
async def home(req: Request):
	return "Welcome home"
```

You want to build a RestAPI? No problem

```py
from wire import Wire, Request


app = Wire()
templates = FoxTemplates("templates")

@app.get("/api")
def api(req: Request):
	return {"name": "Leo", "age": 16}
```

You want to send HTML files? Wire got your back

```py
from wire import Wire, Request
from wire.responses import HTMLResponse


app = Wire()

@app.get("/html")
async def home(req: Request):
	with open("home.html", "r") as f:
		data = f.read()
	return HTMLResponse(data)
```

You want to use some templates ? You want to load templates? No problem with [Fuchs](https://github.com/cheetahbyte/fuchs)

```py
from wire import Wire, Request
from wire.templating import FoxTemplates

app = Wire()
templates = FoxTemplates("templates")

@app.get("/home")
async def home(req: Request):
	return templates.render("home.html", name="Leo")
```

**Changes incoming**

Join our [discord](https://discord.gg/EtqGfBVuZS) !
