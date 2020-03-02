# Start Mongo
## Mac
/Applications/mongodb-macos-x86_64-enterprise-4.2.2/bin/mongod --config /Users/user/Documents/Maria/pymongo/mongod.conf --fork

## Linux
sudo systemctl start mongod

# Stop Mongo
## Mac
ps -efa | grep mongo
look for pid and
kill <pid>

