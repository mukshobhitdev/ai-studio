import dotenv from 'dotenv';
import sql from 'mssql';
import { AzureOpenAI } from "openai";

dotenv.config();

const DEPLOYMENT_NAME = process.env.DEPLOYMENT_NAME;
const API_VERSION = process.env.API_VERSION;

const config = {
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    options: {
        encrypt: false
    }
};

async function getProductById(id) {
    try {
        let pool = await sql.connect(config);
        let result = await pool.request()
            .input('Id', sql.Int, id)
            .query('SELECT Id, Name, Description, CreatedOn FROM Products WHERE Id = @Id');
        return result.recordset[0];
    } catch (err) {
        console.error('SQL error', err);
    }
}

async function deleteProductById(id) {
    try {
        let pool = await sql.connect(config);
        await pool.request()
            .input('Id', sql.Int, id)
            .query('DELETE FROM Products WHERE Id = @Id');
        console.log(`Product with Id ${id} deleted successfully.`);
    } catch (err) {
        console.error('SQL error', err);
    }
}

async function createProduct(name, description) {
    try {
        let pool = await sql.connect(config);
        let result = await pool.request()
            .input('Name', sql.NVarChar, name)
            .input('Description', sql.NVarChar, description)
            .input('CreatedOn', sql.DateTime, new Date())
            .query('INSERT INTO Products (Name, Description, CreatedOn) OUTPUT INSERTED.Id VALUES (@Name, @Description, @CreatedOn)');
        return result.recordset[0].Id;
    } catch (err) {
        console.error('SQL error', err);
    }
}

async function searchProduct(keyword) {
    try {
        let pool = await sql.connect(config);
        let result = await pool.request()
            .input('Keyword', sql.NVarChar, `%${keyword}%`)
            .query('SELECT * FROM Products WHERE Name LIKE @Keyword OR Description LIKE @Keyword');
        return result.recordset;
    } catch (err) {
        console.error('SQL error', err);
    }
}

const client = new AzureOpenAI({ DEPLOYMENT_NAME, API_VERSION });

async function callAzureOpenAI(prompt) {
    try {
        const events = await client.chat.completions.create({
            messages: [
                {
                    role: "user",
                    content:
                        prompt,
                },
            ],
            max_tokens: 128,
            model: DEPLOYMENT_NAME,
        });

        const responseText = events.choices[0].message.content;
        console.log(responseText);
    } catch (error) {
        console.error("Error:", error);
        if (error.status === 404) {
            console.error("Resource not found. Please check the endpoint URL and resource availability.");
        }
    }
}

(async () => {

    await callAzureOpenAI("2 lines about france?");

    // let productId=await createProduct('Sample Product', 'This is a sample mobile.');
    // const product = await getProductById(productId);

    // let searchResponse= await searchProduct('sample');
    // console.log(searchResponse);
    // await deleteProductById(1);
})();
