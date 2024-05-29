document.addEventListener("DOMContentLoaded", function(){

//INIT Html elements

const Box1 = document.getElementById("B1") as HTMLElement;
const Box2 = document.getElementById("B2") as HTMLElement;
const Box3 = document.getElementById("B3") as HTMLElement;
const example = document.getElementById("ex") as HTMLElement;
const counter = document.getElementById("count") as HTMLElement;

//Create function, that will be to make type of examples and true answer

const Math_Operations_Array: string[] = ["-","+","/","*"];


///////////////////////////////////////////////////////////////////////
const create_Examples = (mArr: string[]): string[] =>{

    const randOperation = mArr[Math.floor(Math.random() * mArr.length)];
    let firstNumber: number = Math.round(Math.random() * 100);
    let secondNumber: number = Math.round(Math.random() * 6);

    if(firstNumber === 0){firstNumber = 1};
    if(secondNumber === 0){secondNumber += 1};
    if (!(secondNumber %2 === 0)){secondNumber += 1};
  
    example.textContent = `${firstNumber}${randOperation}${secondNumber}`;

    return [randOperation,`${firstNumber}`,`${secondNumber}`];
  }
///////////////////////////////////////////////////////////////////////



//Create function, that will be to make 3 variables answer

const HTMLElements_BOXES = [Box1,Box2,Box3];

const Micro_Random = ():number =>{return Math.round(Math.random())}

///////////////////////////////////////////////////////////////////////
const three_Var_for_Answer = (): number[] =>{

    const Array = create_Examples(Math_Operations_Array);
    let First = Number(Array[1]);
    let Second = Number(Array[2]);
    let True_answer: number;
    switch (Array[0]){
        case "/":
            True_answer = First / Second 
        break;
        case "*":
            True_answer = First * Second 
        break;
        case "-":
            True_answer = First - Second 
        break;
        case "+":
            True_answer = First + Second 
        break;
        default:
            return [-404]
    }

    const Fake1 = Math.random() * 8;
    const Fake2 = Math.random() * 15;

    if (Micro_Random() === 0){
    First = Math.round((True_answer - Fake1) * 100) / 100;
    Second = Math.round((True_answer + Fake2) * 100) / 100;
    }else{
    First = Math.round((True_answer + Fake1) * 100) / 100;
    Second = Math.round((True_answer - Fake2) * 100) / 100;
    }
    const randBox = HTMLElements_BOXES[Math.round(Math.random() * (HTMLElements_BOXES.length - 1))];
     
    switch (randBox){
        case Box1:
            Box1.textContent = `${Math.round((True_answer * 100)) / 100}`; Box2.textContent = `${Math.round(Second * 100) / 100}`; Box3.textContent = `${Math.round(First * 100) / 100}`;
            break;
        case Box2:
            Box2.textContent = `${Math.round((True_answer * 100)) / 100}`; Box3.textContent = `${Math.round(Second * 100) / 100}`; Box1.textContent = `${Math.round(First * 100) / 100}`;
            break;
        case Box3:
            Box3.textContent = `${Math.round((True_answer * 100)) / 100}`; Box1.textContent = `${Math.round(Second * 100) / 100}`; Box2.textContent = `${Math.round(First * 100) / 100}`;
            break;
    }
    return [True_answer]
}
///////////////////////////////////////////////////////////////////////

//Infinity cycles 
three_Var_for_Answer()

let Speed_Of_Game: number = 3900;
let Counter: number = 0;
counter.textContent = "You score: 0"

const Infinity = setInterval( () => three_Var_for_Answer(), Speed_Of_Game );
  

//Create button function and counter

Box1.addEventListener("click", function(){

})


});
//END