import express from "express";
const router = express.Router();

router.get("/", (req, res) => {
    console.log("on start page here!");
    res.render("index");
});

export default router;
