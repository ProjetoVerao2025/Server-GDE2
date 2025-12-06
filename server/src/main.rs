use sqlx::postgres::PgPoolOptions;
use dotenv::dotenv;
use std::env;

mod models;
mod handlers;
mod config;
mod routes;


#[tokio::main]
async fn main() {
    dotenv().ok();


    // Pegando os dados do .env
    let db_url = env::var("DB_URL").expect("Nao foi possivel obter a url do DB. Abortando\n");


    let port= env::var("SERVER_PORT").unwrap_or_else(|err| {
        eprint!("Nao foi possivel obter a porta: {}. usando o padrao 8000.\n", err);
        "8000".to_string()
    });


    let addr = format!("0.0.0.0:{}", port);


    // Conectando ao banco de dados
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await
        .expect("Nao foi possivel conectar ao banco de dados. Abortando.");




    let app = routes::create_routes().with_state(pool);


    let listener = tokio::net::TcpListener::bind(&addr)
        .await
        .expect("Failed to bind TCP listener");

    println!("Server running on {}", addr);


     axum::serve(listener, app).await.expect("Failed to start server");


}

