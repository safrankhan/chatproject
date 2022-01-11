var tags = 
{
"!top": ["aiml>"],
"!attrs": {
			version:["1.0"],
			encoding:null
		  },
  aiml:{
		  attrs:{
				  lang: ["en", "de", "fr", "nl"],
					  },
		  children: ["topic>","category>"]
	   },

  topic:{
		  attrs:{
				  name:null
				},
		  children:["category>"]
		},

  category:{
			attrs: {
					name: null,
					id: null,
					class:null
				   },
			children: ["pattern>", "template>", "that>"]
		   },

  pattern:{
			attrs:{
					name: null,
					id: null,
					class:null
			},
			children: ["that>","template>","get>","set>","bot>"]
		  },

  that: {
		attrs: {
					   name: null,
				 index: ["1","2","3"],
				 value:null
			   },
		children: ["pattern>", "template>", "that>", "srai>","sr/>" ,"star/>"]
	  },

  template:{
			attrs:{
					name:null,
					id:null,
					class:null
				  },
			children: ["srai>","bot>","get>","star/>","topicstar>","formal>","gossip>","javascript>","learn>","lowercase>","uppercase>","person/>","person2/>","sr/>","random>","system>","sentence>","that>","thatstar>","if>","condition>"]
		  },

  get:{
	  attrs:{
				name:null,
				value:null,
				index:["1","2","3"]
			},
	  children: ["star>","person>","person2>","star/>"]
  },

  set:{
	  attrs:{
			  name:null,
			  value:null,
			  index:["1","2","3"]
			},
	  children:["star>","person>","person2>","star/>"]
  },

  bot:{
	  attrs:{
			  name:null,
			  index:["1","2","3"]
			}
  },

  srai:{
	  attrs:{
			  name:null,
			  value:null,
			  index:["1","2","3"]
			},
	  children:["sr/>","star/>"]      
  },

  star:{
	  attrs:{
			  name:null,
			  index:["1"]
			}
  },

  input:{
		attrs:{
			  name:null,
			  index:["1","2","3"]
			  }
  },

  learn:{
	  attrs:{
			name:null,
			filename:null
			}
  },

  gossip:{
	  attrs:{
			name:null,
			value:null,
			src:null
			},
	  children:["get>","set>","person/>","person2/>"]  
  },

  topicstar:{
	  attrs:{
			name:null,
			index:["1"]
			}
  },

  person:{
	  attrs:{
			name:null,
			value:null,
			index:["1"]
			},
  },

  person2:{
	  attrs:{
			name:null,
			value:null,
			index:["1"]
			},
  },

  random:{
	  children:["li>","set>","get>"]
  },

  thatstar:{
	  attrs:{
			index:["1"]
			}
  },

  if:{
	  attrs:{
			name:null,
			value:null,
			contains:null,
			exists:null
			}
  },

  condition:{
	  attrs:{
			name:null,
			value:null,
			contains:null,
			exists:null
			},
	  children:["li>","set>","get>"]
  },

  li:{
	  attrs:{
			name:null,
			value:null
			},
	  children:["think>","set>","get>","bot>"]
  }
};

function completeAfter(cm, pred) {
var cur = cm.getCursor();
if (!pred || pred()) setTimeout(function() {
  if (!cm.state.completionActive)
	cm.showHint({completeSingle: false});
}, 100);
return CodeMirror.Pass;
}

function completeIfAfterLt(cm) {
return completeAfter(cm, function() {
  var cur = cm.getCursor();
  return cm.getRange(CodeMirror.Pos(cur.line, cur.ch - 1), cur) == "<";
});
}

function completeIfInTag(cm) {
return completeAfter(cm, function() {
  var tok = cm.getTokenAt(cm.getCursor());
  if (tok.type == "string" && (!/['"]/.test(tok.string.charAt(tok.string.length - 1)) || tok.string.length == 1)) return false;
  var inner = CodeMirror.innerMode(cm.getMode(), tok.state).state;
  return inner.tagName;
});
}

var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
mode: "xml",
lineNumbers: true,
extraKeys: {
  "'<'": completeAfter,
  "'/'": completeIfAfterLt,
  "' '": completeIfInTag,
  "'='": completeIfInTag,
  "Ctrl-Space": "autocomplete"
},
hintOptions: {schemaInfo: tags}
});