pyrcc5 main.qrc -o main_rc.py
pyrcc5 resources.qrc -o resources.py

rm -r dist/*
rm -r packages/com.vendor.product/data/*
pyinstaller main.py
#mkdir packages/com.vendor.product/data

cp -r dist/main/* packages/com.vendor.product/data

mv packages/com.vendor.product/data/main packages/com.vendor.product/data/Maria
/home/art/Qt/Tools/QtInstallerFramework/3.1/bin/binarycreator -f -c config/config.xml -p packages Maria-Linux-0.0.1.Setup

