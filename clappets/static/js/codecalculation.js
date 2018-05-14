var app_common = {
    data: {
        userAuthenticated : false,
        username: '',
        successMessage: "",
        successisActive: false,
        warningMessage: "",
        warningisActive: false,
        errorMessage: "",
        errorisActive: false,
        errorStatus:"",
        errors : {},
        selectionMenu: {},
        isLoading: false
    },

    computed : {
        isReadonly: function() {
            if (this.action == "view") {
                return true;
            } else {
                return false;
            }
        },

        id_isReadonly: function() {
            if ((this.action == "edit") || (this.action == "view")) {
                return true;
            } else {
                return false;
            }
        }
    },

    methods : {
        getErrs: function(path_array) {
            val = this.errors;
            total_length = path_array.length;
            try{
                for (i = 0; i < total_length; i++) {
                    key = path_array[i];
                    val = val[key];
                }
                return val;
            }
            catch (err) {
                return [];
            }
        },

        openModal: function(modalisActive) {
            this[modalisActive] = true;
            this.resetMessages();
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');

        },

        closeModal: function(modalisActive) {
            this[modalisActive] = false;
            this.resetMessages();
        },

        hideWarning: function() {
            this.warningisActive = false;
        },

        hideError: function() {
            this.errorisActive = false;
        },

        hideSuccess: function() {
            this.successisActive = false;
        },

        resetMessages: function() {
            this.warningMessage = "";
            this.successMessage = "";
            this.errorStatus = "";
            this.errorMessage = "";
            this.errors = {};
            this.errorisActive = false;
            this.warningisActive = false;
            this.successisActive = false;
        },

        store_messages : function(){
            localStorage["successMessage"] = this.successMessage;
            localStorage["successisActive"] = this.successisActive;
            localStorage["warningMessage"] = this.warningMessage;
            localStorage["warningisActive"] = this.warningisActive;
            localStorage["errorMessage"] = this.errorMessage;
            localStorage["errorisActive"] = this.errorisActive;
        },

        retrieve_messages : function(){
            this.successMessage = localStorage["successMessage"];
            if (localStorage["successisActive"] =="true"){
                this.successisActive = true;
            }
            else{
                this.successisActive = false;
            }
            this.warningMessage = localStorage["warningMessage"];
            if (localStorage["warningisActive"] =="true"){
                this.warningisActive = true;
            }
            else{
                this.warningisActive = false;
            }
            this.errorMessage = localStorage["errorMessage"];
            if (localStorage["errorisActive"] =="true"){
                this.errorisActive = true;
            }
            else{
                this.errorisActive = false;
            }
        },

        login: function(){
            var app = this;
            app.resetMessages();
            var data = {};
            data.username = app.username;
            data.password = app.password;
            var json_data = JSON.stringify(data);
            url = "/auth/";
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    response = JSON.parse(xhr.responseText);
                    app.userAuthenticated = true;
                    localStorage.setItem('access_token', response['access_token']);
                    // use the token received to perform a basic authentication on login test. Browser will rememeber the Credentials
                    // for all future requests and dispatch tokens automatically.
                    url = "/login-test/";
                    token = localStorage["access_token"];
                    var xhr2 = new XMLHttpRequest();
                    xhr2.open("GET", url, true, token, "unused");
                    xhr2.onload = function (e) {
                      if (xhr2.readyState === 4) {
                        if (xhr2.status === 200) {
                            localStorage.setItem('username', app.username);
                            localStorage.setItem('userAuthenticated', app.userAuthenticated);
                            app.successMessage = "User Successfully Logged In"
                            app.successisActive = true;
                            app.loginModalisActive = false;
                            location.href = "/profile";
                        } else {
                          console.error(xhr2.statusText);
                          app.errorMessage = "Login Failed.";
                          app.errorisActive = true;
                        }
                      }
                    };
                    xhr2.onerror = function (e) {
                      console.error(xhr2.statusText);
                      app.errorMessage = "Login Failed.";
                      app.errorisActive = true;
                    };
                    xhr2.send(null);
                }
                else{
                    app.userAuthenticated = false;
                    localStorage.setItem('access_token', 'anonymous');
                    localStorage.setItem('username', app.username);
                    localStorage.setItem('userAuthenticated', app.userAuthenticated);
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(json_data);
        },

        logout: function(){
            var app = this;
            app.resetMessages();
            localStorage.setItem('access_token', 'anonymous');
            localStorage.setItem('username', '');
            localStorage.setItem('userAuthenticated', false);
            token = localStorage["access_token"];
            app.username = localStorage["username"];
            if (localStorage["userAuthenticated"]=="true"){
                app.userAuthenticated = true;
            }
            else{
                app.userAuthenticated = false;
            }
            url = "/login-test/"
            var xhr = new XMLHttpRequest();
            xhr.open("GET", url, true, token, "unused");
            xhr.onload = function (e) {
              if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    app.errorMessage = "Failed to Logout"
                    app.errorisActive = true;
                } else {
                  console.error(xhr.statusText);
                  location.href = "/indexlogin/";
                }
              }
            };
            xhr.onerror = function (e) {
              console.error(xhr.statusText);
            };
            xhr.send(null);
        },

        loadProtectedResource: function(url){
            token = localStorage["access_token"];
            if (typeof token === "undefined") {
                token = "anonymous";
              }
            var xhr = new XMLHttpRequest();
            xhr.open("GET", url, true, token, "unused");
            xhr.onload = function (e) {
              if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    console.log(xhr.responseText);
                    document.location.pathname = url;
                } else {
                    app.errorMessage = xhr.statusText;
                    app.errorisActive = true;
                    console.error(xhr.statusText);
                }
              }
            };
            xhr.onerror = function (e) {
              console.error(xhr.statusText);
            };
            xhr.send(null);
        }, //end of loadProtectedResource

        get_resource_list : function(resource_list, base_url, fn_success) {
            var app = this;
            app.resetMessages();
            url = base_url;
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    app.handle_success_with_content(xhr, resource_list);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(null);
        },


        get_resource: function(resource_name, resource_id, base_url, fn_success) {
            var app = this;
            app.resetMessages();
            url = base_url + resource_id + "/";
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    app.handle_success_with_content(xhr, resource_name);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(null);
        },


        add_resource: function(resource_name, base_url, fn_success) {
            var app = this;
            app.resetMessages();
            url = base_url;
            var data = {};
            data.resource = app[resource_name];
            var json_data = JSON.stringify(data);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            app.isLoading = true;
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "201"){
                    app.handle_success_without_content(xhr);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(json_data);
        },


        update_resource: function(resource_name, resource_id, base_url, fn_success) {
            var app = this;
            app.resetMessages();
            url = base_url + resource_id + '/'
            var data = {};
            data.resource = app[resource_name];
            var json_data = JSON.stringify(data);
            var xhr = new XMLHttpRequest();
            xhr.open('PUT', url, true);
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            xhr.onload = function(e){
                console.log(xhr.responseText);
                if (xhr.readyState == 4 && xhr.status == "200"){
                    app.handle_success_without_content(xhr);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(json_data);
        },

        delete_resource: function(resource_name, resource_id, base_url, fn_success) {
            if (confirm("Want to delete " + resource_id + " in " + resource_name)) {
                var app = this;
                app.resetMessages();
                url = base_url + resource_id + '/';
                var xhr = new XMLHttpRequest();
                xhr.open('DELETE', url, true);
                xhr.onload = function(e){
                    if (xhr.readyState == 4 && xhr.status == "200"){
                        app.handle_success_without_content(xhr);
                        fn_success();
                    }
                    else{
                        app.handle_errors(xhr);
                    }
                };
                xhr.onerror = function (e) {
                    app.handle_connection_errors();
                };
                xhr.send(null);
            }
        },

        process_resource: function(resource_name, base_url, fn_success) {
            var app = this;
            app.resetMessages();
            url = base_url;
            var data = {};
            data[resource_name] = app[resource_name];
            var json_data = JSON.stringify(data);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            app.isLoading = true;
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    app.handle_success_with_content(xhr, resource_name);
                    fn_success();
                }
                else{
                    app.handle_errors(xhr);
                }
            };
            xhr.onerror = function (e) {
                app.handle_connection_errors();
            };
            xhr.send(json_data);
        },

        handle_success_with_content : function(xhr, resource_name){
            console.log(xhr.responseText);
            response = JSON.parse(xhr.responseText);
            this[resource_name] = response;
            this.successMessage = "Data Loaded Successfully"
//            this.successisActive = true;
            this.isLoading = false;
        },

        handle_success_without_content : function(xhr){
            console.log(xhr.responseText);
            response = JSON.parse(xhr.responseText);
            this.successMessage = response["message"];
//            this.successisActive = true;
            if (response.hasOwnProperty("redirect_url")){
                location.href = response["redirect_url"];
            }
            this.isLoading = false;
        },


        handle_errors : function(xhr){
            console.error(xhr.response);
            this.errorStatus = xhr.status + " " + xhr.statusText;
            try {
                response = JSON.parse(xhr.responseText);
                this.errors = response;
                this.errorMessage = response["message"];
                if (typeof this.errorMessage =='undefined'){
                    this.errorMessage = xhr.responseText;
                }
            }
            catch (e) {
                this.errorMessage = xhr.response;
            }
            this.errorisActive = true;
            this.isLoading = false;
        },

        handle_connection_errors : function(){
            this.errorStatus = "Unknown Error";
            this.errorMessage = "Server Response not received";
            this.errorisActive = true;
            this.isLoading = false;
        },


        execQuery: function(query_url) {
            if (query_url.substring(0, 4) == "/api") {
                var app = this;
                url = query_url;
                var xhr = new XMLHttpRequest();
                xhr.open('GET', url, true);
                xhr.onload = function(e){
                    if (xhr.readyState == 4 && xhr.status == "200"){
                        app.handle_success_with_content(xhr, "selectionMenu");
                    }
                    else{
                        app.handle_errors(xhr);
                    }
                };
                xhr.onerror = function (e) {
                    app.handle_connection_errors();
                };
                xhr.send(null);
            } else if (query_url.substring(0, 4) == "/htm") {
                location.href = query_url;
            }
        },


        print: function() {
            window.print();
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');

        },

        pdf_download: function(resource_name, pdf_url) {
            var app = this;
            app.loadingModalisActive =true;
            app.resetMessages();
            url = pdf_url;
            var data = {};
            data.resource = app[resource_name];
            var json_data = JSON.stringify(data);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.responseType = "arraybuffer";
            xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
            xhr.onload = function(e){
                if (xhr.readyState == 4 && xhr.status == "200"){
                    var blob = new Blob([xhr.response], {type: "application/pdf"});
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(blob);
                    link.download = 'PDF Report.pdf';
                    link.click();
                    app.loadingModalisActive =false;
                }
                else{
                    app.errorStatus = xhr.status + " " + xhr.statusText;
                    app.errorMessage = "Error occured in PDF Download"
                    app.errorisActive = true;
                    app.isLoading = false;
                    app.loadingModalisActive =false;
                }
            };
            xhr.onerror = function (e) {
                xhr.responseType = "text";
                app.handle_connection_errors();
                app.loadingModalisActive =false;
            };
            xhr.send(json_data);
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');

        },

        addListItem: function(targetList, list_entry) {
            var lsitem = JSON.parse(JSON.stringify(list_entry));
            targetList.push(lsitem);
        },

        removeListItem: function(targetList, index) {
            targetList.splice(index, 1);
        },

        retSilent: function(obj, path_array) {
            val = obj;
            total_length = path_array.length;
            try{
                for (i = 0; i < total_length; i++) {
                    key = path_array[i];
                    val = val[key];
                }
                return val;
            }
            catch (err) {
                return "";
            }
        },
        launchHelp : function(){
          hurl = this.help_url;
          if (hurl==null){
            hurl = 'http://docs.codecalculation.com/'
          }
          window.open(hurl, 'helpwindow',"height=640,width=960,toolbar=no,menubar=no,scrollbars=no,location=no,status=no");
        }
    },

    beforeMount : function(){
      try{
        this.username = localStorage['username'];
        if (localStorage.getItem("userAuthenticated")=="true"){
              this.userAuthenticated = true;
          }
          else{
              this.userAuthenticated = false;
          }
      }
      catch (e){
        this.username = "";
        this.userAuthenticated = false;
      }
    },



}
