/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** URL base da ViaturaAPI. Definida em .env ou como build-arg no Docker. */
  readonly VITE_API_URL?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
