# Diagrama de Despliegue — Sistema de Gestión para Gimnasios

```mermaid
flowchart LR
    subgraph Cliente
        Browser[Navegador del usuario]
    end
    subgraph Nube_Frontend [Hosting Frontend candidato: Vercel]
        FE[React - Build estatico]
    end
    subgraph Nube_Backend [Hosting Backend candidato: Render o Railway]
        BE[Node.js + Express - API REST]
    end
    subgraph Nube_DB [Hosting Base de Datos candidato: Railway o Supabase]
        DB[(PostgreSQL)]
    end

    Browser -->|HTTPS| FE
    FE -->|HTTPS / JSON| BE
    BE -->|Conexion SQL| DB
```

## Nodos y componentes

| Nodo | Componente desplegado | Comunicación |
|---|---|---|
| Hosting Frontend | Build estático de React | Servido por HTTPS al navegador del usuario |
| Hosting Backend | API REST (Node.js + Express) | Recibe peticiones HTTPS/JSON del frontend |
| Hosting Base de Datos | PostgreSQL | Recibe conexiones SQL exclusivamente del backend |

El frontend no se conecta directamente a la base de datos — toda comunicación pasa por el backend, como se detalla en [`arquitectura.md`](./arquitectura.md).