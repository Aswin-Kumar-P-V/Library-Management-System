function deleteCat(catID){
    fetch('delete-category', {
        method : 'POST',
        body: JSON.stringify({catID : catID}),
    }).then((_res) => {
        window.location.href = "/add-category"
    });
}

function refreshpage(){
    window.parent.location = window.parent.location.href;
} 

function deleteUser(userID){
    fetch("/delete-user", {
        method : "POST",
        body : JSON.stringify({userID : userID}),
    }).then((_res) =>{
        window.location.href = "/view-users"
    });
}