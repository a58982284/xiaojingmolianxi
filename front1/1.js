//作业10
var square = function () {
    var len = 50
    var n = 4
    var angle = 90
    //开始循环
    var i = 0
    while(i<n){
        i++
        forward(len)
        right(angle)
    }
}

//使用函数
square()
forward(20)
var vafhxy = square
vgfhxy()

//

var log = function () {
    console.log.apply(console,arguments)

}
//
var grade = 3;
if(grade<7){
    log('小学生')
}

//
var grade = 8;
if (grade<7){
    log('小学生')
}
else if (grade<10){
    log('初中生')
}
else{
    log('高中生')
}

//求绝对值
var n =1
if(n%2 ==0){
    log('偶数')
}else {
    log('奇数')
}

//
var i =1
while (i<5){
    log(i)
    i++
}
//
var add = function (a,b) {
    return a+b
}
log('add函数的返回值',add(1,2))
var number = add(1,3)
log('add函数的返回值 number',number)

var abs = function (n) {
    if (n<0){
        n=-n
    }
    return n
}

log(abs(0))
log(abs(-8))
log(abs(3))


