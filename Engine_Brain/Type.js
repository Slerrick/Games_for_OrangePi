document.addEventListener("DOMContentLoaded", function () {
    //INIT Html elements
    var Box1 = document.getElementsByClassName("B1");
    var Box2 = document.getElementsByClassName("B2");
    var Box3 = document.getElementsByClassName("B3");
    var example = document.getElementsByClassName("ex");
    //Create function, that will be to make type of examples and true answer
    var Math_Operations_Array = ["-", "+", "/", "*"];
    var create_Examples = function (mArr) {
        var randOperation = mArr[Math.floor(Math.random() * mArr.length)];
        var firstNumber = Math.round(Math.random() * 100);
        var secondNumber = Math.round(Math.random() * 6);
        if (firstNumber === 0) {
            firstNumber = 1;
        }
        ;
        if (secondNumber === 0) {
            secondNumber += 1;
        }
        ;
        if (!(secondNumber % 2 === 0)) {
            secondNumber += 1;
        }
        ;
        return "".concat(firstNumber).concat(randOperation).concat(secondNumber);
    };
    //Tests
    var i = 0;
    while (i < 30) {
        console.log(create_Examples(Math_Operations_Array));
        i += 1;
    }
});
//END
