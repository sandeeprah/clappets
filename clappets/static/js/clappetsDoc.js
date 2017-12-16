var app_doc = {

    data: {
        selectionModalisActive: false,
        unitsModalisActive: false,
        infoModalisActive: false,
        saveAsModalisActive: false,
        macroModalisActive: false,
        uploadModalisActive: false,
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
        dimensions_used: function() {
            dimensions = []
            for (var dimension in this.doc.units) {
                if (this.doc.units.hasOwnProperty(dimension)) {
                    dimensions.push(dimension);
                }
            }
            return dimensions;
        },
        doc_id: function() {
            meta = this.doc['meta'];
            id = meta["projectID"] + "-" + meta["discipline"] + "-" + meta["docCategory"] + "-" + meta["docSubCategory"] + "-" + meta["docClass"] + "-" + meta["docInstance"];
            return id;
        },

        units_used : function(){
            return this.doc['units']
        }
    },

    watch: {
        units_used: {
            handler: function(new_units, old_units) {
                try {
                    console.log(this.doc);
                   this.treeUnitConvert(this.doc, old_units, new_units);
                } catch (err) {
                    console.log("Error in watch handler for units_used");
                }
            },
            deep: true,
            passive: true,
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
        },

        saveDoc: function() {
            mydata = JSON.stringify(this.doc, null, 2);
            save_anchor = this.$refs['save_anchor']
            save_anchor.download = "formData-" + new Date().getTime();
            save_anchor.href = "data:text/plain," + encodeURIComponent(mydata);
            save_anchor.click();
        },

        openDocDB: function() {
            this.execQuery("/api/document/query/");
            app.selectionModalisActive = true;
        },

        saveDocDB: function() {
            if (this.doc['_id'] == "") {
                this.saveAsModalisActive = true;
            } else {
                this.update_resource("doc", this.doc['_id'], "/api/document/db/" )
            }
        },

        saveAsDocDB: function() {
            this.saveAsModalisActive = false;
            this.add_resource("doc", "/api/document/db/");
        },

        deleteDocDB: function() {
            if (this.doc['_id'] == "") {
                alert("Document does not have a valid ID");
                return;
            } else {
                this.delete_resource("doc", this.doc["_id"], "/api/document/db/");
            }
        },


        calculate : function(){
            fn_success =function(){};
            this.process_resource("doc", "/api/document/calculate/", fn_success)
        },

        runMacros : function(){
            alert('u want to run macros');
        }
    }
}
