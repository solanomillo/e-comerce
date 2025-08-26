let form = document.getElementById('promo_codigo')

form.addEventListener('submit',function(e){
    
    e.preventDefault();
    let codigo = this.codigo.value;
    let url = this.action + '?codigo=' + codigo;

    fetch(url)
     .then(response => response.json())
     .then(response => {
        console.log(response.total);
     })
})