from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import TimeStampMixin, UUIDMixin


class Genre(TimeStampMixin, UUIDMixin):
    name = models.TextField(_("Name"), unique=True)
    description = models.TextField(_("Description"), blank=True)

    class Meta:  # pyright: ignore[]
        db_table = 'content"."genre'
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")

    def __str__(self):
        return f"Genre {self.name}"


class FilmWork(TimeStampMixin, UUIDMixin):
    class FilmWorkType(models.TextChoices):
        MOVIE = "MV", _("Movie")
        TV_SHOW = "TS", _("Tv_show")

    title = models.TextField(_("Titile"))
    description = models.TextField(
        _("Description"),
        blank=True,
    )
    creation_date = models.DateField(
        _("Creation_date"),
        auto_now_add=True,
        null=True,
    )
    file_path = models.TextField(
        _("File Path"),
        blank=True,
    )
    rating = models.FloatField(
        _("Rating"),
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(_("Type"), max_length=2, choices=FilmWorkType.choices)
    genres = models.ManyToManyField(
        Genre,
        verbose_name=_("genres"),
        through="GenreFilmWork",
        related_name="film_works",
    )

    class Meta:  # pyright: ignore[]
        db_table = 'content"."film_work'
        verbose_name = _("FilmWork")
        verbose_name_plural = _("FilmWork")
        indexes = [models.Index(fields=["creation_date"])]

    def __str__(self):
        return f"FilmWork {self.title}"


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(
        FilmWork,
        on_delete=models.CASCADE,
        related_name="genre_film_works",
        verbose_name=_("FilmWorks"),
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="genre_film_works",
        verbose_name=_("Genre"),
    )
    created_at = models.DateTimeField(_("Created"), auto_now_add=True, null=True)

    class Meta:  # pyright: ignore[]
        db_table = 'content"."genre_film_work'
        verbose_name = _("GenreFilmWork")
        verbose_name_plural = _("GenreFilmWork")
        constraints = [
            models.UniqueConstraint(
                fields=["genre", "film_work"], name="unique_film_genre"
            )
        ]
        indexes = [
            models.Index(
                fields=["genre", "film_work"],
                name="genre_film_work_idx",
            ),
        ]

    def __str__(self):
        return f"M2M Table FilmWork film_work-{self.film_work}|genre-{self.genre}"


class Person(UUIDMixin, TimeStampMixin):
    full_name = models.TextField(_("Full name"), unique=True)

    class Meta:  # pyright: ignore[]
        db_table = 'content"."person'
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")

    def __str__(self):
        return f"Person {self.full_name}"


class PersonFilmWork(UUIDMixin):
    class RoleType(models.TextChoices):
        ACTOR = "actor", _("Actor")
        DIRECTOR = "director", _("Director")
        WRITER = "writer", _("Writer")

    film_work = models.ForeignKey(
        FilmWork,
        verbose_name=_("Film work"),
        on_delete=models.CASCADE,
        related_name="person_film_works",
    )
    person = models.ForeignKey(
        Person,
        verbose_name=_("Person"),
        on_delete=models.CASCADE,
        related_name="person_film_works",
    )
    role = models.CharField(_("role"), max_length=8, choices=RoleType.choices)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:  # pyright: ignore[]
        db_table = 'content"."person_film_work'
        verbose_name = _("PersonFilmWork")
        verbose_name_plural = _("PersonFilmWorks")
        constraints = [
            models.UniqueConstraint(
                fields=["film_work_id", "person_id", "role"],
                name="unique_film_person_role",
            )
        ]
        indexes = [
            models.Index(
                fields=["film_work_id", "person_id", "role"],
                name="film_work_person_role_idx",
            ),
        ]

    def __str__(self):
        return f"PersonFilmWork {self.film_work}"
