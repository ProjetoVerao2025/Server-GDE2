use sqlx::postgres::PgPool;
use sqlx::postgres::PgPoolOptions;
use dotenv::dotenv;
use std::env;

mod models;
mod handlers;
mod config;
mod routes;


// Inicializando o banco de dados
async fn run_migrations(pool: &PgPool) -> Result<(), sqlx::Error> {
    sqlx::migrate!("./migrations").run(pool).await?;
    Ok(())
}

#[tokio::main]
async fn main() {
    dotenv().ok();


    // Pegando os dados do .env
    let db_url = env::var("DB_URL").expect("Nao foi possivel obter a url do DB. Abortando\n");


    let port= env::var("SERVER_PORT").unwrap_or_else(|err| {
        eprintln!("Nao foi possivel obter a porta: {}. usando o padrao 8000.\n", err);
        "8000".to_string()
    });


    let addr = format!("0.0.0.0:{}", port);


    // Conectando ao banco de dados
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await
        .expect("Nao foi possivel conectar ao banco de dados. Abortando.");



    let migration_result = run_migrations(&pool)
        .await;

    match migration_result {
        Ok(res) => {
            println!("Migrations ran successfully");

        }

        Err(err) => {
            eprintln!("Migration Error: {}", err)
        }
        
    }

    let app = routes::create_routes().with_state(pool);


    let listener = tokio::net::TcpListener::bind(&addr)
        .await
        .expect("Failed to bind TCP listener");

    println!("Server running on {}", addr);


     axum::serve(listener, app).await.expect("Failed to start server");


}

