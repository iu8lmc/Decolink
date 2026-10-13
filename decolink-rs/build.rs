// Collega libopus solo con la feature `opus`. La cartella delle librerie e' quella
// di MSYS2 (mingw64/lib); si puo' cambiare con OPUS_LIB_DIR.
fn main() {
    println!("cargo:rerun-if-env-changed=OPUS_LIB_DIR");
    let dir = std::env::var("OPUS_LIB_DIR").unwrap_or_else(|_| "C:/msys64/mingw64/lib".into());
    if std::env::var_os("CARGO_FEATURE_OPUS").is_some() || std::env::var_os("CARGO_FEATURE_HAMLIB").is_some() {
        println!("cargo:rustc-link-search=native={dir}");
    }
    if std::env::var_os("CARGO_FEATURE_OPUS").is_some() {
        println!("cargo:rustc-link-lib=opus");
    }
    if std::env::var_os("CARGO_FEATURE_HAMLIB").is_some() {
        println!("cargo:rustc-link-lib=hamlib");
    }
}
