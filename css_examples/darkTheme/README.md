# Dark Theme for Vantiq Web Client

* ```gmapNightMode.js``` - Add as a custom asset to give google maps widgets a night time theme. 

Add this code to the page on start. Make sure to change the getWidget name to the one used in your client.
```
var mapWidget = client.getWidget("DynamicMapViewer");
var map = mapWidget.map;
map.setOptions({"styles":gmapNightStyle});
```

Upload the .thm file to vantiq/themes/DarkTheme.thm and it will appear in the Client properties Theme page. 

Upload the css file and add it as a custom asset to fill in some blanks not covered in the Theme settings (fixes added to 1.31 to correct this)