//数组和
var sum = function(array){
    var s = 0
    for (var i = 0; i < array.length; i++) {
        var n = array[i]
        s =s+n
    }
    return s
}
sum([1,2,3,4,56,78,9])

var sum = function(array){
    var s = 1
    for (var i = 0; i < array.length; i++) {
        var n = array[i]
        s = s*n
    }
    return s
}
sum([1,2,3,4,56,78,9])

//函数绝对值
var abs = function(n){
    if (n<0) {
        return -n
    }
    else {
        return n
    }
}
abs(-10)
//使用 while 循环计算 100 内的奇数和
var n =1
var sum = 0
while (n<=100) {
    if (n%2==1) {
        sum = sum + n
    }
    n +=1
}
console.log('1 到 100 的奇数和是', sum);

//
var i = 0
while(i < 10) {
    log('while 中的 break 语句')
    // break 语句执行后, 循环就结束了
    break
    // 因此 i += 1 这一句是不会被执行的
    i += 1
}

console.log('break 结束的 i 值', i)
//
var i = 0
while (i<10) {
    i+=1
    if (i%2==0) {
        continue
    }
    console.log('while 中的 contine 语句', i);
}
//object
var taoer = {
    'name':'li',
    'height':'184',
}
console.log('object',taoer);
//
var gua = {
    name: 'xiaogua',
    height: 169,
}
gua['sex'] = '男'
console.log('object增加',gua);
//
delete gua.sex
console.log('object删除',gua);
//递归阶乘
var fac = function(n){
    if (n==0) {
        return 1
    }else {
        return n * fac(n-1)
    }
}
fac(10)
//斐波那契数列
var fib = function (n) {
    if (n==1||n==2) {
        return 1
    }else {
        return fib(n-2)+fib(n-1)
    }
}
console.log(fib(8));
