import json
import logging

from schema2md.contexts import Context
from schema2md.declarations import *
from schema2md.format_funcs import bold, code, italic, quote
from schema2md.reference import Reference

LOGGER = logging.getLogger()


def parse_schema(ctx: Context, schema_title: str):
    schema = ctx.globalc.schema

    ctx.write("# " + schema_title)
    ctx.write_empty()

    ctx.write("## Root Properties")
    for (k, _) in schema.get(PROPERTIES_KEY, {}).items():  # type: ignore
        ctx.write(f"- [{k}](#{k.lower()})")

    ctx.write_empty()
    ctx.write("<br>")
    ctx.write_empty()

    if DESCRIPTION_KEY in schema:
        ctx.write(schema[DESCRIPTION_KEY] + "<br>")  # type: ignore

    ctx.write_empty()
    show_examples(schema, ctx)

    ctx.write_empty()
    ctx.write("<br>")
    ctx.write_empty()

    ctx.write("-------------------------------")
    for (k, v) in schema.get(PROPERTIES_KEY, {}).items():  # type: ignore
        ctx.write(f"### {k}")
        ctx.write("([Back to top](#root-properties))")
        ctx.write_empty()
        parse(v, ctx.indent().append_to_keyspath(k).append_to_objectpath(schema))
        ctx.write("-------------------------------")


def parse(o: JObj, ctx: Context):
    if REFERENCE_KEY in o:
        parse_reference(o, ctx)
    elif ENUM_TYPE in o and TYPE_KEY not in o:
        parse_pure_enum(o, ctx)
    elif o.get(TYPE_KEY) == OBJECT_TYPE:
        parse_object_type(o, ctx)
    elif o.get(TYPE_KEY) == ARRAY_TYPE:
        parse_array_type(o, ctx)
    elif o.get(TYPE_KEY) in VALUE_TYPES:
        parse_value_type(o, ctx)
    elif any(k in o for k in COMPOSITION_KEYS):
        parse_oneOrAnyOrAll_of(o, ctx)
    else:
        LOGGER.warn(f"Unparsed object with format {o}")


def summarise(o: JObj, ctx: Context, title_override: str = ""):
    # Construct top single header line
    path: str = "." + ctx.keyspath_excluding_root
    path_info = (
        f"(Path from root: {italic(code(path))})" if len(ctx.keyspath) > 1 else ""
    )
    if TYPE_KEY in o:
        type_description = f"type {italic(code(o[TYPE_KEY]))}"  # type: ignore
        if ctx.parent_obj.get(TYPE_KEY) == ARRAY_TYPE and not title_override:
            ctx.write(f"- ({type_description}) {path_info}<br>")
        else:
            title: str = title_override or ctx.current_key
            ctx.write(
                f"- {bold(code(quote(title)))} {bold(italic('REQUIRED*')) if ctx.is_required else ''} ({type_description}) {path_info}<br>"
            )
    elif ENUM_TYPE in o:
        ctx.write(
            f"- {bold(code(quote(ctx.current_key)))} {bold(italic('REQUIRED*')) if ctx.is_required else ''} (type: **`Enum`**) {path_info}<br>"
        )
    elif any(k in o for k in COMPOSITION_KEYS):
        key = next((k for k in COMPOSITION_KEYS if k in o))
        ctx.write(
            f"- {bold(code(quote(ctx.current_key)))} {bold(italic('REQUIRED*')) if ctx.is_required else ''} (type: {bold(code(key.title()))}) {path_info}<br>"
        )

    # Defaults
    if DEFAULT_KEY in o:
        ctx.write(f"Default value: {italic(code(o[DEFAULT_KEY]))}<br>")  # type: ignore

    # Deprecated, readonly, etc.
    misc_statements = [
        f"Value is {italic(code(key))}. "
        for key in (DEPRECATED_KEY, READONLY_KEY, WRITEONLY_KEY)
        if o.get(key) == True
    ]
    if misc_statements:
        ctx.write("Attributes: " + "; ".join(misc_statements) + "<br>")

    # Description
    if DESCRIPTION_KEY in o:
        ctx.write(f"{o[DESCRIPTION_KEY]}<br>")


def show_examples(o: JObj, ctx: Context):
    if EXAMPLES_KEY in o:
        ctx.write_empty()
        ctx.indent(1).write("<br>" + italic("Examples:"))
        for example in o[EXAMPLES_KEY]:  # type: ignore
            ctx.indent(1).write("- ```json")
            for line in json.dumps(example, indent=4).split("\n"):
                ctx.indent(2).write(line)
            ctx.indent(2).write("```")
        ctx.indent(2).write("")


def parse_object_type(o: JObj, ctx: Context):
    summarise(o, ctx)
    show_examples(o, ctx)

    if o.get(ADDITIONAL_PROPERTIES_KEY) == True:
        ctx.write(
            f"**Additional Properties**: additional properties on this object are `allowed`<br>"
        )

    if PROPERTIES_KEY in o:
        parse_properties(o, ctx)
    elif any(k in o for k in COMPOSITION_KEYS):
        parse_oneOrAnyOrAll_of(o, ctx)


def parse_value_type(o: JObj, ctx: Context):
    summarise(o, ctx)
    parse_enum_constraints(o, ctx)

    if o[TYPE_KEY] == STRING_TYPE:
        parse_string_constraints(o, ctx)
    elif o[TYPE_KEY] in (NUMBER_TYPE, INTEGER_TYPE):
        parse_number_constraints(o, ctx)

    show_examples(o, ctx)


def parse_pure_enum(o: JObj, ctx: Context):
    summarise(o, ctx)
    parse_enum_constraints(o, ctx)


def parse_enum_constraints(o: JObj, ctx: Context):
    if ENUM_TYPE in o:
        enums: str = ", ".join(italic(code(quote(e))) for e in o[ENUM_TYPE])  # type: ignore
        ctx.write(f"**Constraint (Enum):** Value must be ONE of: [{enums}]<br>")


def parse_string_constraints(o: JObj, ctx: Context):
    if any(k in o for k in STRING_CONSTRAINT_KEYS):

        if MIN_LENGTH_KEY in o:
            ctx.indent().write(
                f"**Constraint:** Value must be at least {code(o[MIN_LENGTH_KEY])} characters long<br>"  # type: ignore
            )
        elif MAX_LENGTH_KEY in o:
            ctx.indent().write(
                f"**Constraint:** Value must be at most {code(o[MAX_LENGTH_KEY])} characters long<br>"  # type: ignore
            )

        if PATTERN_KEY in o:
            ctx.indent().write(
                f"**Constraint:** Value must match regular expression: {code(o[PATTERN_KEY])}<br>"  # type: ignore
            )

        if FORMAT_KEY in o:
            ctx.indent().write(f"**Constraint:** Value must match format of: {code(o[FORMAT_KEY])}<br>")  # type: ignore


def parse_number_constraints(o: JObj, ctx: Context):
    if any(k in o for k in NUMBER_CONSTRAINT_KEYS):

        if MULTIPLE_OF_KEY in o:
            ctx.indent().write(
                f"**Constraint:** Value must be a multiple of {code(o[MULTIPLE_OF_KEY])}<br>"  # type: ignore
            )

        if EXCLUSIVE_MIN_KEY in o:
            ctx.indent().write(f"**Constraint:** Value must be strictly greater than {code(o[EXCLUSIVE_MIN_KEY])}<br>")  # type: ignore
        elif MIN_KEY in o:
            ctx.indent().write(f"**Constraint:** Value must be greater than or equal to {code(o[MIN_KEY])}<br>")  # type: ignore

        if EXCLUSIVE_MAX_KEY in o:
            ctx.indent().write(f"**Constraint:** Value must be strictly less than {code(o[EXCLUSIVE_MAX_KEY])}<br>")  # type: ignore
        elif MAX_KEY in o:
            ctx.indent().write(f"**Constraint:** Value must be less than or equal to {code(o[MAX_KEY])}<br>")  # type: ignore


def parse_reference(o: JObj, ctx: Context):
    ref: Reference = Reference(o[REFERENCE_KEY])  # type: ignore

    parent_is_object_type: bool = ctx.parent_obj.get(TYPE_KEY) == OBJECT_TYPE

    if ref not in ctx.localc.reference_history:
        if parent_is_object_type:
            parse(
                o=ctx.resolve_global_reference(ref),
                ctx=ctx.mark_local_reference_as_seen(ref).append_to_objectpath(o),
            )
        else:
            parse(
                o=ctx.resolve_global_reference(ref),
                ctx=ctx.append_to_keyspath(ref.key)
                .mark_local_reference_as_seen(ref)
                .append_to_objectpath(o),
            )
    else:
        upstream_path: str = ctx.localc.reference_history[ref]
        title: str = ctx.current_key if parent_is_object_type else ref.key
        summarise(ctx.resolve_global_reference(ref), ctx, title_override=title)
        ctx.write(
            f"-**`This is a Recursive object`**, with the same definition and properties as {italic(code(upstream_path))}"
        )


def parse_array_type(o: JObj, ctx: Context):
    summarise(o, ctx)
    show_examples(o, ctx)

    if ITEMS_KEY in o:
        ctx.write(f"***<br>Each item of {ctx.current_key} array must be:<br>***")
        ctx.indent().write("[")
        ctx.write_empty()

        item: JObj = o[ITEMS_KEY]  # type: ignore
        parse(o=item, ctx=ctx.indent().append_to_objectpath(o))

        ctx.write_empty()
        ctx.indent().write("&shy; ]")
    else:
        LOGGER.warn(f"No items key found in array {o}")


def parse_properties(o: JObj, ctx: Context):
    ctx.write(f"**<br>Inner Properties of {ctx.current_key}:<br>**")
    ctx.indent().write("{")
    ctx.write_empty()

    for (key, value) in o[PROPERTIES_KEY].items():  # type: ignore
        parse(o=value, ctx=ctx.indent().append_to_keyspath(key).append_to_objectpath(o))

    ctx.write_empty()
    ctx.indent().write("&shy; }")


def parse_oneOrAnyOrAll_of(o: JObj, ctx: Context):
    summarise(o, ctx)

    key = next((k for k in COMPOSITION_KEYS if k in o))

    ctx.write(
        f"***<br>This object can take {key.title()} the following forms (total of `{len(o[key])}` variations):<br>***"  # type: ignore
    )
    ctx.indent().write("[")
    ctx.write_empty()

    for (i, option_object) in enumerate(o[key], 1):  # type: ignore
        parse(
            o=option_object,
            ctx=ctx.indent()
            .append_to_keyspath("{" + key + "}")
            .append_to_objectpath(o),
        )

    ctx.write_empty()
    ctx.indent().write("&shy; ]")
