document.addEventListener("DOMContentLoaded", function () {
    //INIT Html elements
    var Box1 = document.getElementById("B1");
    var Box2 = document.getElementById("B2");
    var Box3 = document.getElementById("B3");
    var example = document.getElementById("ex");
    var counter = document.getElementById("count");
    //Create function, that will be to make type of examples and true answer
    var Math_Operations_Array = ["-", "+", "/", "*"];
    ///////////////////////////////////////////////////////////////////////
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
        example.textContent = "".concat(firstNumber).concat(randOperation).concat(secondNumber);
        return [randOperation, "".concat(firstNumber), "".concat(secondNumber)];
    };
    ///////////////////////////////////////////////////////////////////////
    //Create function, that will be to make 3 variables answer
    var HTMLElements_BOXES = [Box1, Box2, Box3];
    var Micro_Random = function () { return Math.round(Math.random()); };
    ///////////////////////////////////////////////////////////////////////
    var three_Var_for_Answer = function () {
        var Array = create_Examples(Math_Operations_Array);
        var First = Number(Array[1]);
        var Second = Number(Array[2]);
        var True_answer;
        switch (Array[0]) {
            case "/":
                True_answer = First / Second;
                break;
            case "*":
                True_answer = First * Second;
                break;
            case "-":
                True_answer = First - Second;
                break;
            case "+":
                True_answer = First + Second;
                break;
            default:
                return [-404];
        }
        var Fake1 = Math.random() * 8;
        var Fake2 = Math.random() * 15;
        if (Micro_Random() === 0) {
            First = Math.round((True_answer - Fake1) * 100) / 100;
            Second = Math.round((True_answer + Fake2) * 100) / 100;
        }
        else {
            First = Math.round((True_answer + Fake1) * 100) / 100;
            Second = Math.round((True_answer - Fake2) * 100) / 100;
        }
        var randBox = HTMLElements_BOXES[Math.round(Math.random() * (HTMLElements_BOXES.length - 1))];
        switch (randBox) {
            case Box1:
                Box1.textContent = "".concat(Math.round((True_answer * 100)) / 100);
                Box2.textContent = "".concat(Math.round(Second * 100) / 100);
                Box3.textContent = "".concat(Math.round(First * 100) / 100);
                break;
            case Box2:
                Box2.textContent = "".concat(Math.round((True_answer * 100)) / 100);
                Box3.textContent = "".concat(Math.round(Second * 100) / 100);
                Box1.textContent = "".concat(Math.round(First * 100) / 100);
                break;
            case Box3:
                Box3.textContent = "".concat(Math.round((True_answer * 100)) / 100);
                Box1.textContent = "".concat(Math.round(Second * 100) / 100);
                Box2.textContent = "".concat(Math.round(First * 100) / 100);
                break;
        }
        return [True_answer];
    };
    ///////////////////////////////////////////////////////////////////////
    //Infinity cycles 
    three_Var_for_Answer();
    var Speed_Of_Game = 3900;
    var Counter = 0;
    counter.textContent = "You score: 0";
    var Infinity = setInterval(function () { return three_Var_for_Answer(); }, Speed_Of_Game);
    //Create button function and counter
    Box1.addEventListener("click", function () {
    });
});
//END
