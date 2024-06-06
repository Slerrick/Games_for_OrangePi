// Adding DOM Event Handlers
document.addEventListener("DOMContentLoaded", function () {

  //Try get value from localStorage
  let Counter_var: number = 0;
  try {
    Counter_var = Number(localStorage.getItem("Counter_var_sker"));
  } catch (error) {
    console.log("Var do not init");
    localStorage.setItem("Counter_var_sker", "0");

  }

  // Initializing HTML elements
  const Button_Easy = document.getElementById("easy") as HTMLElement;
  const Button_Hard = document.getElementById("hard") as HTMLElement;
  const Box1 = document.getElementById("B1") as HTMLElement;
  const Box2 = document.getElementById("B2") as HTMLElement;
  const Box3 = document.getElementById("B3") as HTMLElement;
  const example = document.getElementById("ex") as HTMLElement;
  const counter = document.getElementById("count") as HTMLElement;
  const Box1_div = document.getElementById("DB1") as HTMLElement;
  const Box2_div = document.getElementById("DB2") as HTMLElement;
  const Box3_div = document.getElementById("DB3") as HTMLElement;
  const Button_1 = document.getElementById("But-1") as HTMLElement;

  // Creating a function that will generate examples and the correct answer
  let Math_Operations_Array: string[] = ["-", "+", "/", "*"];

  const create_Examples = (mArr: string[]): string[] => {

    const randOperation = mArr[Math.floor(Math.random() * mArr.length)];
    let firstNumber: number = Math.round(Math.random() * 100);
    let secondNumber: number = Math.round(Math.random() * 6);

    if (firstNumber === 0) { firstNumber = 1 };
    if (secondNumber === 0) { secondNumber += 1 };
    if (!(secondNumber % 2 === 0)) { secondNumber += 1 };

    example.textContent = `${firstNumber}${randOperation}${secondNumber}`;

    return [randOperation, `${firstNumber}`, `${secondNumber}`];
  };

  // Creating a function that will generate 3 possible answers, one of which will be correct
  const HTMLElements_BOXES = [Box1, Box2, Box3];

  const Micro_Random = (): number => { return Math.round(Math.random()) };

  const three_Var_for_Answer = (): number => {

    const Array = create_Examples(Math_Operations_Array);
    let First = Number(Array[1]);
    let Second = Number(Array[2]);
    let True_answer: number;
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
        return -404
    }

    const Fake1 = Math.random() * 8;
    const Fake2 = Math.random() * 4;

    if (Micro_Random() === 0) {
      First = Math.round((True_answer - Fake1) * 100) / 100;
      Second = Math.round((True_answer + Fake2) * 100) / 100;
    } else {
      First = Math.round((True_answer + Fake1) * 100) / 100;
      Second = Math.round((True_answer - Fake2) * 100) / 100;
    }
    const randBox = HTMLElements_BOXES[Math.round(Math.random() * (HTMLElements_BOXES.length - 1))];

    switch (randBox) {
      case Box1:
        Box1.textContent = `${Math.round((True_answer * 100)) / 100}`; Box2.textContent = `${Math.round(Second * 100) / 100}`; Box3.textContent = `${Math.round((First)) * 100 / 100}`;
        break;
      case Box2:
        Box2.textContent = `${Math.round((True_answer * 100)) / 100}`; Box3.textContent = `${Math.round(Second * 10) / 10}`; Box1.textContent = `${Math.round(First * 100) / 100}`;
        break;
      case Box3:
        Box3.textContent = `${Math.round((True_answer * 100)) / 100}`; Box1.textContent = `${Math.round((Second * 100) / 100)}`; Box2.textContent = `${Math.round(First * 10) / 10}`;
        break;
    }
    return True_answer
  };

  // Endless loops and settings

  // settings_VARIABLES
  let Speed_Of_Game: number = 3900;
  let One_click: number = 1;
  let Check_Answer: number = 0;
  counter.textContent = `Ваш счет:${localStorage.getItem("Counter_var_sker")}`;
  
  //Start examples
  Check_Answer = Math.round(three_Var_for_Answer() * 100) / 100;

  let Infinity_Game = setInterval(() => { Check_Answer = Math.round(three_Var_for_Answer() * 100) / 100; console.log(Check_Answer) }, Speed_Of_Game);
  let One_click_block = setInterval(() => { One_click = 1 }, Speed_Of_Game);
  const Save_Counter_var = setInterval(() => { localStorage.setItem("Counter_var_sker", `${Counter_var}`) }, 4000);

  // Creating a button and counter function
  const B11 = (number_box: number): void | any => {
    if (HTMLElements_BOXES[number_box].textContent == `${Check_Answer}` && One_click == 1) {
      Counter_var += 1;
      One_click = 0;
      counter.textContent = `Ваш счет: ${Counter_var}`
    } else {
      Counter_var -= 4;
      One_click = 0;
      counter.textContent = `Ваш счет: ${Counter_var}`
    };
  }

  //RESET SCORE
  const Reset = () =>{
    Counter_var = 0;
    localStorage.setItem("Counter_var_sker", "0")
    counter.textContent = "Ваш счет: 0";
  }

  Box1_div.addEventListener("click", () => B11(0));

  Box2_div.addEventListener("click", () => B11(1));

  Box3_div.addEventListener("click", () => B11(2));

  Button_1.addEventListener("click", () => Reset());
  

  //Buttons logic
  let Is_easy: boolean = true;
  let Is_hard: boolean = false;

  Button_Easy.addEventListener("click", () =>{

      Button_Easy.style.backgroundColor = 'rgba(16, 156, 60, 0.5)';
      Button_Hard.style.backgroundColor = 'rgba(6, 56, 30, 0.1)';

      Is_hard = false
      Is_easy = true

      Level_Of_Game(true)
  })
  Button_Hard.addEventListener("click", () =>{

      Button_Hard.style.backgroundColor = 'rgba(16, 156, 60, 0.5)';
      Button_Easy.style.backgroundColor = 'rgba(6, 56, 30, 0.1)';

      Is_easy = false
      Is_hard = true

      Level_Of_Game(false)
  })

  const Level_Of_Game = (easy: boolean) => {
    if (easy){
    clearInterval(Infinity_Game);
    clearInterval(One_click_block);

    Speed_Of_Game = 3900;
    Math_Operations_Array = ["-", "+", "/", "*"];

    Infinity_Game = setInterval(() => { Check_Answer = Math.round(three_Var_for_Answer() * 100) / 100; console.log(Check_Answer) }, Speed_Of_Game);
    One_click_block = setInterval(() => { One_click = 1 }, Speed_Of_Game);
    }else{
    clearInterval(Infinity_Game);
    clearInterval(One_click_block);

    Speed_Of_Game = 2000;
    Math_Operations_Array = ["/", "*"];

    Infinity_Game = setInterval(() => { Check_Answer = Math.round(three_Var_for_Answer() * 100) / 100; console.log(Check_Answer) }, Speed_Of_Game);
    One_click_block = setInterval(() => { One_click = 1 }, Speed_Of_Game);
    }
  }
});
//END