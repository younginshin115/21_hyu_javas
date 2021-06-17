
# Command line instructions
You can also upload existing files from your computer using the instructions below.


# Git global setup
git config --global user.name "KYOUGYUN LEE"
git config --global user.email "skyblue.lee@gmail.com"

# 새 저장소 만들기
git clone https://gitlab.com/hy21-pbl-chat-analysis/hy21-pbl-chat-analysis.git
cd hy21-pbl-chat-analysis
git switch -c main
touch README.md
git add README.md
git commit -m "add README"
git push -u origin main

# Push an existing folder
cd existing_folder
git init --initial-branch=main
git remote add origin https://gitlab.com/hy21-pbl-chat-analysis/hy21-pbl-chat-analysis.git
git add .
git commit -m "Initial commit"
git push -u origin main

# Push an existing Git repository
cd existing_repo
git remote rename origin old-origin
git remote add origin https://gitlab.com/hy21-pbl-chat-analysis/hy21-pbl-chat-analysis.git
git push -u origin --all
git push -u origin --tags
