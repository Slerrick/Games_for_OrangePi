console.log("Hello,world!");

import fs;

let Data = {
    win: true,
    lose: false
}

let send = JSON.stringify(Data)

fs.writeFile('user.json', Data, (err) => {
    if (err) {
        console.log('Error writing file:', err);
    } else {
        console.log('Successfully wrote file');
    }
});