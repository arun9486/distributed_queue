# Tasks
* create Queue
* send message
* receive message
* delete message
** complete cleanup
* clean up after retention
* visibility timeout



## Visibility
For visibility we can do simply polling. With prefix like INPROGREES_<timestamp > current> something like that
but for scalability we can define a node (got from a leader) and that node is responisble for cleaning
deleting records etc


## RPC Server
Support mult-threading of RPC server