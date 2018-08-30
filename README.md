# Linebot 說明以及 ubuntu 環境說明
## 查詢anaconda當前環境以及啟動gaston虛擬環境
```
conda info --envs
source activate gaston
```
成功啟動環境後會發現環境成功切換，此部份用來安裝新套件

## 啟動linebot
```
sudo ~/anaconda3/envs/gaston/bin/python app.py
```
root password: hellohello

## Open the mysql database
```
mysql -u root -p
```
root password: hellohello
Manage database using GUI application - MySQL Workbench

## The structure of this api
controller : App route
model : SQL ORM
sc-dictionary : Traditional chinese dictionary

## Quick open sublime editor
```
subl .
subl [file name]
```

## Open ngrok
```
ngrok http [port]
```


