    try{
    this.username = localStorage.getItem("username");
    if (localStorage.getItem("userAuthenticated")=="true"){
        this.userAuthenticated = true;
    }
    else{
        this.userAuthenticated = false;
    }
}catch(e){
    this.username = "";
    this.userAuthenticated = false;
    localStorage.setItem('access_token', 'anonymous');
}

if (this.username==null){
    this.username = "";
    try{
      localStorage.setItem('access_token', 'anonymous');
    }

}
