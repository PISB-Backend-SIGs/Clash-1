
// to handle instruction page
document.getElementById("instruction_checkbox").addEventListener("change",()=>{
    let instruction_btn=document.getElementById("instruction_submit_btn");
    if (instruction_btn.disabled === true){
        instruction_btn.disabled = false;
    }else{
        instruction_btn.disabled =true;
    }
})