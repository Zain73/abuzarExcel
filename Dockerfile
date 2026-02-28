FROM python:3.12-slim

RUN apt-get update && apt-get install -y libreoffice && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY convert.py .

CMD ["python3", "convert.py"]
```

---

**Step 2: Deploy on Render**

1. Go to [render.com](https://render.com) → Sign up / Log in
2. Click **New** → **Web Service**
3. Connect your GitHub account → select the `xls-converter` repo
4. Fill in the settings:
   - **Name:** xls-converter (anything)
   - **Environment:** `Docker`
   - **Region:** pick closest to you
   - **Instance Type:** `Free`
5. Click **Deploy Web Service**

It'll take a few minutes the first time (LibreOffice is a big install). Once done you'll get a URL like:
```
https://xls-converter.onrender.com
