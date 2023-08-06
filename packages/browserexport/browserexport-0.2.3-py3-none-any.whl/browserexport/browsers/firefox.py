from .common import (
    Iterator,
    Visit,
    Metadata,
    PathIshOrConn,
    Browser,
    unquote,
    Path,
    Schema,
    _execute_query,
    _from_datetime_microseconds,
    _func_if_some,
    _handle_glob,
    _handle_path,
)


class Firefox(Browser):
    detector = "SELECT * FROM moz_meta, moz_annos"
    schema = Schema(
        cols=[
            "P.url",
            # Hack to tell apart whether timestamp is stored in microseconds (on desktop) or in milliseconds (on mobile)
            # We set 300_000_000 as threshold, it's year 1979, so definitely before Firefox existed,
            # and the same multipied by 1000 is year 11476, also enough time for us not to care.
            "(CASE WHEN (V.visit_date > 300000000 * 1000000) THEN V.visit_date ELSE V.visit_date * 1000 END) AS visit_date",
            "V.visit_date",
            "P.title",
            "P.description",
            "P.preview_image_url",
        ],
        where="FROM moz_historyvisits as V, moz_places as P WHERE V.place_id = P.id",
        order_by="V.visit_date",
    )

    @classmethod
    def extract_visits(cls, path: PathIshOrConn) -> Iterator[Visit]:
        for row in _execute_query(path, cls.schema.query):
            yield Visit(
                url=unquote(row["url"]),
                dt=_from_datetime_microseconds(row["visit_date"]),
                metadata=Metadata.make(
                    title=row["title"],
                    description=row["description"],
                    preview_image=_func_if_some(row["preview_image_url"], unquote),
                ),
            )

    @classmethod
    def data_directory(cls) -> Path:
        return _handle_path(
            {
                "linux": "~/.mozilla/firefox/",
                "darwin": "~/Library/Application Support/Firefox/Profiles/",
            },
            browser_name=cls.__name__,
        )

    @classmethod
    def locate_database(cls, profile: str = "*") -> Path:
        dd: Path = cls.data_directory()
        return _handle_glob(dd, profile + "/places.sqlite")
