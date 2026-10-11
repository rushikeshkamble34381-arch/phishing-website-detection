{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "121b87e1-1d06-42a2-89ef-90e94eb7ee73",
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (1125588924.py, line 1)",
     "output_type": "error",
     "traceback": [
      "\u001b[1;36m  Cell \u001b[1;32mIn[2], line 1\u001b[1;36m\u001b[0m\n\u001b[1;33m    cd C:\\Users\\rushi\\Desktop\\PhishGuard\u001b[0m\n\u001b[1;37m       ^\u001b[0m\n\u001b[1;31mSyntaxError\u001b[0m\u001b[1;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "cd C:\\Users\\rushi\\Desktop\\PhishGuard\n",
    "python -m streamlit run app.py"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "3148cf0d-3824-4532-9742-e2d337ca983e",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "C:\\Users\\rushi\\Desktop\\PhishGuard\n"
     ]
    }
   ],
   "source": [
    "cd C:\\Users\\rushi\\Desktop\\PhishGuard"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "951f8a0d-f5c2-45f6-838d-691bc14f3fa1",
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (2436129529.py, line 1)",
     "output_type": "error",
     "traceback": [
      "\u001b[1;36m  Cell \u001b[1;32mIn[6], line 1\u001b[1;36m\u001b[0m\n\u001b[1;33m    python -m streamlit run app.py\u001b[0m\n\u001b[1;37m              ^\u001b[0m\n\u001b[1;31mSyntaxError\u001b[0m\u001b[1;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "python -m streamlit run app.py"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "de7a52db-ebf4-498c-96be-e777820d5370",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-10-10 19:30:16.438 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\rushi\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n",
      "2026-10-10 19:30:16.514 Session state does not function when running a script without `streamlit run`\n"
     ]
    }
   ],
   "source": [
    "\n",
    "import streamlit as st\n",
    "\n",
    "st.set_page_config(\n",
    "    page_title=\"PhishGuard\",\n",
    "    page_icon=\"🛡️\"\n",
    ")\n",
    "\n",
    "st.title(\"🛡️ PhishGuard\")\n",
    "st.subheader(\"Phishing Website Detection\")\n",
    "\n",
    "url = st.text_input(\n",
    "    \"Enter a website URL\",\n",
    "    placeholder=\"https://example.com\"\n",
    ")\n",
    "\n",
    "if st.button(\"Check Website\"):\n",
    "    if not url.strip():\n",
    "        st.warning(\"Please enter a URL.\")\n",
    "    else:\n",
    "        st.info(\n",
    "            \"URL received: \" + url.strip()\n",
    "        )\n",
    "        st.warning(\n",
    "            \"This is the initial interface. \"\n",
    "            \"ML prediction will be connected after the model integration is verified.\"\n",
    "        )\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "1d399c92-e569-420a-aa5a-d0904660cbdf",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "\n",
    "st.set_page_config(page_title=\"PhishGuard\", page_icon=\"🛡️\")\n",
    "\n",
    "st.title(\"🛡️ PhishGuard\")\n",
    "st.subheader(\"Phishing Website Detection\")\n",
    "\n",
    "url = st.text_input(\"Enter a website URL\")\n",
    "\n",
    "if st.button(\"Check Website\"):\n",
    "    if url.strip():\n",
    "        st.write(\"URL entered:\", url.strip())\n",
    "        st.warning(\"This is a frontend test. ML prediction is not connected yet.\")\n",
    "    else:\n",
    "        st.error(\"Please enter a URL.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "11848c3a-c32e-4242-8b6c-6da448a89b2e",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
