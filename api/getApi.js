'use strict'

var div_resultado=document.querySelector("#resultados");
var noticias=[]

//Envía la consulta al servidor
function enviarDatos(){
    let div_formulario= document.querySelector("#formulario"); //JQuery
    let consulta_var= div_formulario.consulta.value
    let orden_var= div_formulario.orden.value
    //Funciones promesa 
    //Fectch || ajax
    fetch('http://192.168.100.2:5000/consulta',
        {
            method:"POST",
            body: JSON.stringify({
                consulta: consulta_var,
                orden: orden_var
            }
            
            ),
            headers:{
                'Content-Type': 'application/json'}
        }
    ).then(data=>res=> res.json())
    .catch(error=> console.error('Error: ', error))
    .then(response => console.log('Success: ',response));
}


//Obtenemos las fichas técnicas del servidor
fetch('http://192.168.100.2:5000/',
    {
        method: "GET",

    })
    .then(data =>data.json())   
	.then(data => {
		listadoNoticia(data); //Se cargan visualmente las noticias en el Front-End
});


//Crea un apartado para cada noticia del documento de fichas técnicas
function listadoNoticia(noticia){
    noticia.map((nota, i)=>{
        console.log(nota);
        let resultado= document.createElement('div');  //Se crea una sección para la noticia
        resultado.innerHTML= crearNoticia(nota); //Se agrega el HTML de la noticia ya con sus respectivo formato
        div_resultado.appendChild(resultado); //Se añade la sección al HTML del Buscador
    });
}

//Otorga el formato HTML a la noticia 
function crearNoticia(noticia){
    return `
    <div class="container resultado">
            <div class="row">
                <div class="col text-center"> 
                    <h1 class="letra-resultado">`+noticia.titulo +`</h1>
                </div>

            </div>
            <div class="row align-items-center">                
                <div class="col-md-8 ">
                    <a href="`+ noticia.ref +`" target="_blank">
                        <img class="imagen-nota" src="`+ noticia.img +`">
                    </a>
                </div>
                <div class="letra-resumen col-md-4 d-none d-sm-block">
                    <p>Autor: `+ noticia.autor +`</p>
                    <p>Numero de Gaceta: `+ noticia.gaceta +`</p>
                    <p>Fecha: `+ noticia.fecha + `</p>
                </div>
            </div>
            <div class="row letra-resumen">
                <p>
                    `+ noticia.resumen +`
                </p>
            </div>
        </div>
        <br><br>
    `
    ;
}



