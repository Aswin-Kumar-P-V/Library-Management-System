function deleteCat(catID){
    fetch('delete-category', {
        method : 'POST',
        body: JSON.stringify({catID : catID}),
    }).then((_res) => {
        window.location.href = "/add-category"
    });
}