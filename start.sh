if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Botsthe/Aa.git /Aa
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Aa
fi
cd /Aa
pip3 install -U -r requirements.txt
echo "Starting Aa 😎...."
python3 bot.py    
