'use strict'

var div_resultado=document.querySelector("#resultados");
var noticias=[]

//Envía la consulta al servidor
function enviarDatos(){
    div_resultado.innerHTML="";
    let div_formulario= document.querySelector("#formulario"); //JQuery
    let consulta_var= div_formulario.consulta.value
    let orden_var= div_formulario.orden.value
    postearDatos(consulta_var, orden_var);
    //Funciones promesa 
    //Fectch || ajax
    /*
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

    ).then(function(){
        obtener_datos();
    })
    .catch(error=> console.error('Error: ', error))
    .then(response => console.log('Success: ',response));
            }*/

    
}

function postearDatos(consulta_var, orden_var){
    const http= new XMLHttpRequest();

    http.open("POST", 'http://127.0.0.1:5000/consulta');
    http.setRequestHeader("Content-Type","application/json")
    http.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            console.log(this.responseText);
            obtener_datos();
        }
    }
    http.send(JSON.stringify({
        consulta: consulta_var,
        orden: orden_var
    }));
}


//Obtenemos las fichas técnicas del servidor

function obtener_datos(){
    const http= new XMLHttpRequest();

    http.open("GET", 'http://127.0.0.1:5000/resultados');
    http.setRequestHeader("Content-Type","application/json")
    http.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var resultado= JSON.parse(this.responseText);
            listadoNoticia(resultado);
        }
    }
    http.send();
}



/*function obtener_datos(){
    fetch('http://192.168.100.2:5000/resultados',
        {
            method: "GET",
    
        })
        .then(data =>data.json())   
        .then(data => {
            console.log("data:")
            console.log(data);
            listadoNoticia(data); //Se cargan visualmente las noticias en el Front-End
    });}
*/

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



