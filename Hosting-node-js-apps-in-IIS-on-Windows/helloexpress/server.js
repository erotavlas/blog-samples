const Express = require('express');

const app = Express();

app.get('/helloexpress', (req, res)=>{
    res.send("hello")
})

app.listen(process.env.PORT)

