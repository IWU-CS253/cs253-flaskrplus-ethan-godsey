function filterPost(){
    const filter = document.querySelector("#filter");
    const entries = document.querySelectorAll(".entries li");
    const selected_category = filter.value

    entries.forEach(entry=>{
        const any_category = entry.querySelector("h4").innerHTML
        if (selected_category === "All" || any_category === selected_category){
            entry.style.display = "block"
        }
        else {
            entry.style.display = "none"
        }
    })
}
