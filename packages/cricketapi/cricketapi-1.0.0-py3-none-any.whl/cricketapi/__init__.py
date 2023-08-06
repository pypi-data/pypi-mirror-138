def featured_matches() -> str:
    from cricketapi.request_handlers.apis import RzApp
    return RzApp().featured_matches_summary()