var log = function(){
    console.log.apply(console,arguments)
}

var ensure = function(condition,message){
    if(!condition)
       {log('*** 测试失败:', message)}

}




var find = function(s1,s2){
    var len = s1.length
    if(s1.includes(s2)){
        for(var i = 0; i<len; i++){
            var str = s1[i]
            if (str==s2){
                return i
            }
        }
    }
    return -1
}
