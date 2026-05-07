## 🚀 𝐃𝐞𝐩𝐥𝐨𝐲𝐦𝐞𝐧𝐭 𝐆𝐮𝐢𝐝𝐞

<details>
<summary><b>📦 𝐕𝐏𝐒 𝐃𝐞𝐩𝐥𝐨𝐲𝐦𝐞𝐧𝐭 (𝐂𝐥𝐢𝐜𝐤 𝐭𝐨 𝐄𝐱𝐩𝐚𝐧𝐝)</b></summary>

<br>

### **𝐒𝐭𝐞𝐩 𝟏: 𝐔𝐩𝐝𝐚𝐭𝐞 𝐒𝐲𝐬𝐭𝐞𝐦**

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

---

### **𝐒𝐭𝐞𝐩 𝟐: 𝐈𝐧𝐬𝐭𝐚𝐥𝐥 𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐏𝐚𝐜𝐤𝐚𝐠𝐞𝐬**

```bash
sudo apt-get install python3 python3-pip ffmpeg git screen curl -y
```

---

### **𝐒𝐭𝐞𝐩 𝟑: 𝐈𝐧𝐬𝐭𝐚𝐥𝐥 𝐍𝐨𝐝𝐞.𝐣𝐬**

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
```

```bash
sudo apt-get install -y nodejs
```

---

### **𝐒𝐭𝐞𝐩 𝟒: 𝐂𝐥𝐨𝐧𝐞 𝐑𝐞𝐩𝐨𝐬𝐢𝐭𝐨𝐫𝐲**

```bash
git clone https://github.com/NoxxOP/ShrutiMusic
```

```bash
cd ShrutiMusic
```

---

### **𝐒𝐭𝐞𝐩 𝟓: 𝐂𝐫𝐞𝐚𝐭𝐞 𝐒𝐜𝐫𝐞𝐞𝐧 𝐒𝐞𝐬𝐬𝐢𝐨𝐧**

```bash
screen
```

**𝐍𝐨𝐭𝐞:** Press `Ctrl+A` then `D` to detach screen

**𝐓𝐨 𝐑𝐞𝐚𝐭𝐭𝐚𝐜𝐡:**
```bash
screen -ls
```
```bash
screen -r {screen_id}
```

---

### **𝐒𝐭𝐞𝐩 𝟔: 𝐈𝐧𝐬𝐭𝐚𝐥𝐥 𝐕𝐢𝐫𝐭𝐮𝐚𝐥 𝐄𝐧𝐯𝐢𝐫𝐨𝐧𝐦𝐞𝐧𝐭 𝐏𝐚𝐜𝐤𝐚𝐠𝐞**

```bash
sudo apt-get install python3-venv -y
```

---

### **𝐒𝐭𝐞𝐩 𝟕: 𝐂𝐫𝐞𝐚𝐭𝐞 𝐕𝐢𝐫𝐭𝐮𝐚𝐥 𝐄𝐧𝐯𝐢𝐫𝐨𝐧𝐦𝐞𝐧𝐭**

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

### **𝐒𝐭𝐞𝐩 𝟖: 𝐈𝐧𝐬𝐭𝐚𝐥𝐥 𝐏𝐲𝐭𝐡𝐨𝐧 𝐃𝐞𝐩𝐞𝐧𝐝𝐞𝐧𝐜𝐢𝐞𝐬**

```bash
pip3 install -U pip
```

```bash
pip3 install -U -r requirements.txt
```

---

### **𝐒𝐭𝐞𝐩 𝟗: 𝐂𝐨𝐧𝐟𝐢𝐠𝐮𝐫𝐚𝐭𝐢𝐨𝐧**

```bash
nano .env
```

**𝐅𝐢𝐥𝐥 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐯𝐚𝐫𝐢𝐚𝐛𝐥𝐞𝐬:**

- `API_ID` & `API_HASH` - Get from [my.telegram.org](https://my.telegram.org)
- `BOT_TOKEN` - Get from [@BotFather](https://t.me/BotFather)
- `MONGO_DB_URI` - MongoDB Atlas connection string
- `OWNER_ID` - Your Telegram user ID
- `STRING_SESSION` - Generate using [@Sessionbbbot](https://t.me/Sessionbbbot)
- `LOG_GROUP_ID` - Log group/channel ID (starting with -100)
- `SUPPORT_GROUP` - Your support group link
- `SUPPORT_CHANNEL` - Your support channel link

**Save:** `Ctrl+X` then `Y` then `Enter`

---

### **𝐒𝐭𝐞𝐩 𝟏𝟎: 𝐒𝐭𝐚𝐫𝐭 𝐁𝐨𝐭**

**𝐌𝐞𝐭𝐡𝐨𝐝 𝟏:**
```bash
python3 -m ShrutiMusic
```

**𝐌𝐞𝐭𝐡𝐨𝐝 𝟐:**
```bash
bash start
```

**𝐃𝐞𝐭𝐚𝐜𝐡 𝐒𝐜𝐫𝐞𝐞𝐧:** `Ctrl+A` then `D`

</details>

---

<p align="center">
<a href="https://t.me/The_LuckyX"> <img src="https://img.shields.io/badge/𝐋𝚄𝙲𝙺𝚈 𝐑𝙰𝙹𝙰-darkred?style=for-the-badge&logo=telegram" alt="PritiMusic" /> </a>
</p>

---

### 🔧 Quick Setup

1. **Upgrade & Update:**
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. **Install Required Packages:**
   ```bash
   sudo apt-get install python3-pip ffmpeg -y
   ```
3. **Setting up PIP**
   ```bash
   sudo pip3 install -U pip
   ```
4. **Installing Node**
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash && source ~/.bashrc && nvm install v18
   ```
5. **Clone the Repository**
   ```bash
   git clone https://github.com/Im-NotCoder/PtaHai && cd PtaHai
   ```
6. **Install Requirements**
   ```bash
   pip3 install -U -r requirements.txt
   ```
7. **Create .env  with sample.env**
   ```bash
   cp sample.env .env
   ```
   - Edit .env with your vars
8. **Editing Vars:**
   ```bash
   vi .env
   ```
   - Edit .env with your values.
   - Press `I` button on keyboard to start editing.
   - Press `Ctrl + C`  once you are done with editing vars and type `:wq` to save .env or `:qa` to exit editing.
9. **Installing tmux**
    ```bash
    sudo apt install tmux -y && tmux
    ```
10. **Run the Bot**
    ```bash
    bash start
    ```

---