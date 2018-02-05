var app_doc = {

    data: {
        selectionModalisActive: false,
        unitsModalisActive: false,
        infoModalisActive: false,
        saveAsModalisActive: false,
        macroModalisActive: false,
        uploadModalisActive: false,
        loadingModalisActive: false,
        api_url : {
            doc : "/api/document/db/"
        },
        pdf_url : {
            doc : "/pdf/document/"
        },
        macro_url: {

        }
    },

    computed : {
        doc_id: function() {
            meta = this.doc['meta'];
            id = meta["projectID"] + "-" + meta["discipline"] + "-" + meta["docCategory"] + "-" + meta["docSubCategory"] + "-" + meta["docClass"] + "-" + meta["docInstance"];
            return id;
        },
        dimensions_used: function() {
            dimensions = []
            for (var dimension in this.doc.units) {
                if (this.doc.units.hasOwnProperty(dimension)) {
                    dimensions.push(dimension);
                }
            }
            return dimensions;
        },
        units_used : function(){
          var clone = JSON.parse(JSON.stringify(this.doc.units))
          return clone;
        },
        show_units : function(){
          return true;
        },

        show_calculation: function(){
          return true;
        }

    },

    watch: {
        'units_used': {
            handler: function(new_units, old_units) {
                try {
                   this.treeUnitConvert(this.doc, old_units, new_units);
                } catch (err) {
                    console.log("Error in watch handler for units_used");
                }
            },
            deep: true,
        }
    },

    methods : {
        gUL: function(dimension) {
            try {
                unitUsed = this.doc.units[dimension]
                unitLabel = getUnitLabel(dimension, unitUsed)
                return unitLabel
            } catch (err) {
                console.log("Error occured in getUnitLabel trying to fetch unitUsed '" + unitUsed + "'")
                return '';
            }
        },

        getUnits: function(dimension) {
            try {
                return getUnits(dimension)
            } catch (err) {
                console.log("Error occured in getUnits with dimension = '" + dimension + "'");
            }
        },

        treeUnitConvert : function(tree, fromUnits, toUnits){
            treeUnitConvert(tree, fromUnits, toUnits);
        },

        newDoc: function() {
            this.execQuery("/api/document/tpl/");
            app.selectionModalisActive = true;
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');

        },

        saveDoc: function() {
            mydata = JSON.stringify(this.doc, null, 2);
            save_anchor = this.$refs['save_anchor']
            save_anchor.download = "formData-" + new Date().getTime();
            save_anchor.href = "data:text/plain," + encodeURIComponent(mydata);
            save_anchor.click();
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');
        },

        openDocDB: function() {
            this.execQuery("/api/document/query/");
            app.selectionModalisActive = true;
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');
        },

        saveDocDB: function() {
            if (this.doc['_id'] == "") {
                this.saveAsModalisActive = true;
            } else {
                this.update_resource("doc", this.doc['_id'], "/api/document/db/" )
            }
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');
        },

        saveAsDocDB: function() {
            this.saveAsModalisActive = false;
            this.add_resource("doc", "/api/document/db/");
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');
        },

        deleteDocDB: function() {
            if (this.doc['_id'] == "") {
                alert("Document does not have a valid ID");
                return;
            } else {
                this.delete_resource("doc", this.doc["_id"], "/api/document/db/");
            }
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');
        },

        calculate : function(){
            fn_success =function(){};
            this.doc['result'] ={};
            this.doc['errors'] =[];
            this.process_resource("doc", "/api/document/calculate/", fn_success);
            burgerMain = document.getElementById('burgerMain');
            navMenu = document.getElementById('navMenu');
            burgerMain.classList.remove('is-active');
            navMenu.classList.remove('is-active');
        },

        runMacros : function(){
            alert('u want to run macros');
        }
    }
}
