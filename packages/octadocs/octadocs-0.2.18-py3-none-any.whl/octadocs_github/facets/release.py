from datetime import date, datetime

from dominate.tags import code, a, span, br
from more_itertools import first

from iolanta.facet import Facet


class Release(Facet):
    """Render a software project release."""

    sparql = '''
    SELECT * WHERE {
        $release
            gh:published_at ?date ;
            gh:name ?name .

        OPTIONAL {
            $release gh:prerelease ?prerelease .
        }
    }
    '''

    def render(self):
        """Draw release description."""
        rows = self.query(
            self.sparql,
            release=self.iri,
        )

        row = first(rows)

        date_value = row['date'].value

        if isinstance(date_value, datetime):
            date_value = date_value.date()

        return span(
            code(str(date_value)),
            br(),
            a(
                row['name'],
                href=row['release'],
            ),
            cls='octadocs-github-release',
        )
