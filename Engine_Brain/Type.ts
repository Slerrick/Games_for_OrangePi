document.addEventListener("DOMContentLoaded", function(){

//INIT Html elements

const Box1 = document.getElementsByClassName("B1");
const Box2 = document.getElementsByClassName("B2");
const Box3 = document.getElementsByClassName("B3");
const example = document.getElementsByClassName("ex");

//Create function, that will be to make type of examples and true answer

const Math_Operations_Array: string[] = ["-","+","/","*"];


///////////////////////////////////////////////////////////////////////
const create_Examples = (mArr: string[]): string =>{

    const randOperation = mArr[Math.floor(Math.random() * mArr.length)];
    let firstNumber: number = Math.round(Math.random() * 100);
    let secondNumber: number = Math.round(Math.random() * 6);

    if(firstNumber === 0){firstNumber = 1};
    if(secondNumber === 0){secondNumber += 1};
    if (!(secondNumber %2 === 0)){secondNumber += 1};
  
    return `${firstNumber}${randOperation}${secondNumber}`;
  }
///////////////////////////////////////////////////////////////////////




//Tests
let i = 0;
while (i < 30) {
    console.log(create_Examples(Math_Operations_Array));
    i += 1;
}



});
//END