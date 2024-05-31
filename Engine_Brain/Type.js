// Adding DOM Event Handlers
document.addEventListener("DOMContentLoaded", function () {
    //Try get value from localStorage
    var Counter_var = 0;
    try {
        Counter_var = Number(localStorage.getItem("Counter_var_sker"));
    }
    catch (error) {
        console.log("Var do not init");
        localStorage.setItem("Counter_var_sker", "0");
    }
    // Initializing HTML elements
    var Box1 = document.getElementById("B1");
    var Box2 = document.getElementById("B2");
    var Box3 = document.getElementById("B3");
    var example = document.getElementById("ex");
    var counter = document.getElementById("count");
    var Box1_div = document.getElementById("DB1");
    var Box2_div = document.getElementById("DB2");
    var Box3_div = document.getElementById("DB3");
    var Button_1 = document.getElementById("But-1");
    // Creating a function that will generate examples and the correct answer
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
        example.textContent = "".concat(firstNumber).concat(randOperation).concat(secondNumber);
        return [randOperation, "".concat(firstNumber), "".concat(secondNumber)];
    };
    // Creating a function that will generate 3 possible answers, one of which will be correct
    var HTMLElements_BOXES = [Box1, Box2, Box3];
    var Micro_Random = function () { return Math.round(Math.random()); };
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
                return -404;
        }
        var Fake1 = Math.random() * 8;
        var Fake2 = Math.random() * 4;
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
                Box3.textContent = "".concat(Math.round((First)) * 100 / 100);
                break;
            case Box2:
                Box2.textContent = "".concat(Math.round((True_answer * 100)) / 100);
                Box3.textContent = "".concat(Math.round(Second * 10) / 10);
                Box1.textContent = "".concat(Math.round(First * 100) / 100);
                break;
            case Box3:
                Box3.textContent = "".concat(Math.round((True_answer * 100)) / 100);
                Box1.textContent = "".concat(Math.round((Second * 100) / 100));
                Box2.textContent = "".concat(Math.round(First * 10) / 10);
                break;
        }
        return True_answer;
    };
    // Endless loops and settings
    // settings_VARIABLES
    var Speed_Of_Game = 3900;
    var One_click = 1;
    var Check_Answer = 0;
    counter.textContent = "\u0412\u0430\u0448 \u0441\u0447\u0435\u0442:".concat(localStorage.getItem("Counter_var_sker"));
    //Start examples
    Check_Answer = Math.round(three_Var_for_Answer() * 100) / 100;
    var Infinity = setInterval(function () { Check_Answer = Math.round(three_Var_for_Answer() * 100) / 100; console.log(Check_Answer); }, Speed_Of_Game);
    var One_click_block = setInterval(function () { One_click = 1; }, Speed_Of_Game);
    var Save_Counter_var = setInterval(function () { localStorage.setItem("Counter_var_sker", "".concat(Counter_var)); }, Speed_Of_Game * 2);
    // Creating a button and counter function
    var B11 = function (number_box) {
        if (HTMLElements_BOXES[number_box].textContent == "".concat(Check_Answer) && One_click == 1) {
            Counter_var += 1;
            One_click = 0;
            counter.textContent = "\u0412\u0430\u0448 \u0441\u0447\u0435\u0442: ".concat(Counter_var);
        }
        else {
            Counter_var -= 4;
            One_click = 0;
            counter.textContent = "\u0412\u0430\u0448 \u0441\u0447\u0435\u0442: ".concat(Counter_var);
        }
        ;
    };
    //RESET SCORE
    var Reset = function () {
        Counter_var = 0;
        localStorage.setItem("Counter_var_sker", "0");
        counter.textContent = "Ваш счет: 0";
    };
    Box1_div.addEventListener("click", function () { return B11(0); });
    Box2_div.addEventListener("click", function () { return B11(1); });
    Box3_div.addEventListener("click", function () { return B11(2); });
    Button_1.addEventListener("click", function () { return Reset(); });
});
//END
