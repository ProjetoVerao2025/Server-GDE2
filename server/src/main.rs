use std::env;

mod handlers;
mod models;
mod routes;
mod db;

// Inicializando o banco de dados

#[tokio::main]
async fn main() {
    let port = env::var("SERVER_PORT").unwrap_or_else(|err| {
        eprintln!(
            "Nao foi possivel obter a porta: {}. usando o padrao 8000.\n",
            err
        );
        "8000".to_string()
    });

    let addr = format!("0.0.0.0:{}", port);

    let pool = db::prepare_db().await;

    let app = routes::create_routes().with_state(pool);

    let listener = tokio::net::TcpListener::bind(&addr)
        .await
        .expect("Failed to bind TCP listener");

    println!("Server running on {}", addr);

    axum::serve(listener, app)
        .await
        .expect("Failed to start server");
}
