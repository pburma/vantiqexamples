### White Label Example

This example includes some additional files used to white label the deployment. This can extend to the IDE view as well as the user run time components like the Web Client.

This feature is full documented here [White Labeling Vantiq](https://dev.vantiq.com/docs/system/idebranding/index.html#white-labeling-vantiq)

Additional files should be added to this folder. 

1. webUIConfig.json
2. brandedProperties
3. Any custom image files

The samples below are taken from the online documentation. Make sure to include the image files in your docker\-compose.yml to make sure they get mounted properly into the platform. The customizations made to the docker yaml is primarily to mount the additional files into the container and is otherwise just like the simple example.

**Sample webUIConfig.json**

```
{
  "loadGoogleComponents": true,
  "loadBaiduComponents": false,

  "brandedProperties": "override.properties",

  "navbarDefaults": {
      "backgroundColor": "#1e6cb6",
      "titleColor": "#ffffff",
      "titleFontWeight": "400",
      "titleFontFamily": "'Source Sans Pro', Helvetica, Arial, sans-serif",
      "titleFontStyle": "normal",
      "titleFontSize": 20,
      "appicon": "myAppIcon.png",
      "icon": "myNavbarIcon.png",
      "iconHeight": 26,
      "iconWidth": 98,
      "height": 50,
      "titleTopPadding": 0,
      "iconTopPadding": 12
  }
}
```

**Sample brandedProperties**

```
core.company.name = Vantiq
core.product.name = Vantiq
core.privacy.policy = https://vantiq.com/wp-content/uploads/VANTIQ-Privacy-Policy.pdf
core.terms.and.conditions = http://vantiq.com/vantiq-terms-services
core.modelo.title = Vantiq - Modelo
core.pronto.title = Vantiq - Pronto
core.rtc.title = Vantiq Client Launcher
core.mpi.title = Vantiq Launcher
core.drp.title = Vantiq Request Processor
core.orgWebsite = http://www.vantiq.com
core.supportUrl = support@vantiq.com
core.forumUrl = http://stackoverflow.com/questions/tagged/vantiq
core.modelo.name = Modelo
core.modelo.full.name = Modelo Full
core.modelo.light.name = Modelo Light
core.pronto.name = Pronto
core.platform.name = Platform
core.configProntoMod = Configure Pronto and Modelo

```
