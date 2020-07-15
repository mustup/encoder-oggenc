import logging
import shlex

import mustup.core.encoder
import mustup.core.tup.rule

logger = logging.getLogger(
    __name__,
)


class Encoder(
            mustup.core.encoder.Encoder,
        ):
    supported_extensions = {
        '.wave',
    }

    supported_transformations = {
    }

    # oggenc offers shortcuts for some common tags
    tag_parameter_map = {
        'album': '--album',
        'artist': '--artist',
        'title': '--title',
        'track number': '--tracknum',
    }

    # opusenc offers shortcuts for some Vorbis comments
    vorbiscomment_parameter_map = {
        'DATE': '--date',
    }

    def process_directory(
                self,
                metadata,
            ):
        try:
            pictures = metadata['pictures']['APIC']
        except KeyError:
            pass
        else:
            vorbis_comment_files = [
            ]

            iterator = pictures.items(
            )

            for picture_type, details in iterator:
                path = details['path']

                picture_type_base10 = str(
                    picture_type,
                )

                output_name = f'picture-{ picture_type_base10 }.vc'

                command=[
                    'mustup-mbp',
                    '--type',
                    picture_type_base10,
                    '--path',
                    shlex.quote(
                        path,
                    ),
                    '--output',
                    output_name,
                ]

                try:
                    description = details['description']
                except KeyError:
                    pass
                else:
                    command.append(
                        '--description',
                    )
                    command.append(
                        shlex.quote(
                            description,
                        ),
                    )

                rule = mustup.core.tup.rule.Rule(
                    inputs=[
                        path,
                    ],
                    caret_flags=[
                        'o',
                    ],
                    command=command,
                    outputs=[
                        output_name,
                    ],
                )

                rule.output(
                )

                vorbis_comment_files.append(
                    output_name,
                )

            command = [
                'cat',
                '--',
            ]

            command.extend(
                vorbis_comment_files,
            )

            command.append(
                '>',
            )

            command.append(
                'pictures.vc',
            )

            rule = mustup.core.tup.rule.Rule(
                inputs=vorbis_comment_files,
                command=command,
                outputs=[
                    'pictures.vc',
                ],
            )

            rule.output(
            )

    def process_track(
                self,
                metadata,
                source_basename,
                source_name,
                transformations,
            ):
        output_name = f'{ source_basename }.ogg'

        inputs = [
            source_name,
        ]

        command = [
            '@(OGGENC)',
            '@(OGGENC_FLAGS)',
        ]

        try:
            tags = metadata['tags']
        except KeyError:
            pass
        else:
            command.append(
                '--utf8',
            )

            # Tags are sorted to ensure consistent ordering of the command line arguments.
            # If ordering varied, tup would run the commands again.

            try:
                common_tags = tags['common']
            except KeyError:
                pass
            else:
                iterator = Format.tag_parameter_map.items(
                )

                sorted_pairs = sorted(
                    iterator,
                )

                for pair in sorted_pairs:
                    tag_key = pair[0]
                    parameter = pair[1]
                    try:
                        value = common_tags[tag_key]
                    except KeyError:
                        pass
                    else:
                        multiple_values = isinstance(
                            value,
                            list,
                        )

                        if multiple_values:
                            vorbis_comment_values = value

                            for vorbis_comment_value in vorbis_comment_values:
                                command.append(
                                    parameter,
                                )

                                argument = shlex.quote(
                                    vorbis_comment_value,
                                )

                                command.append(
                                    argument,
                                )
                        else:
                            vorbis_comment_value = value

                            command.append(
                                parameter,
                            )

                            argument = shlex.quote(
                                vorbis_comment_value,
                            )

                            command.append(
                                argument,
                            )

            try:
                vorbis_comments = tags['Vorbis']
            except KeyError:
                pass
            else:
                iterator = vorbis_comments.items(
                )

                sorted_pairs = sorted(
                    iterator,
                )

                for pair in sorted_pairs:
                    vorbis_comment_key = pair[0]
                    value = pair[1]

                    multiple_values = isinstance(
                        value,
                        list,
                    )

                    if multiple_values:
                        vorbis_comment_values = value

                        for vorbis_comment_value in vorbis_comment_values:
                            try:
                                parameter = Format.vorbiscomment_parameter_map[vorbis_comment_key]
                            except KeyError:
                                parameter = '--comment'

                                argument = shlex.quote(
                                    f'{ vorbis_comment_key }={ vorbis_comment_value }',
                                )
                            else:
                                argument = shlex.quote(
                                    vorbis_comment_value,
                                )

                            command.append(
                                parameter,
                            )

                            command.append(
                                argument,
                            )
                    else:
                        vorbis_comment_value = value

                        try:
                            parameter = Format.vorbiscomment_parameter_map[vorbis_comment_key]
                        except KeyError:
                            parameter = '--comment'

                            argument = shlex.quote(
                                f'{ vorbis_comment_key }={ vorbis_comment_value }',
                            )
                        else:
                            argument = shlex.quote(
                                vorbis_comment_value,
                            )

                        command.append(
                            parameter,
                        )

                        command.append(
                            argument,
                        )

        command.extend(
            [
                '--output',
                shlex.quote(
                    output_name,
                ),
                '--',
                shlex.quote(
                    source_name,
                ),
            ],
        )

        try:
            pictures = metadata['pictures']['APIC']
        except KeyError:
            pass
        else:
            command.extend(
                [
                    '&&',
                    'vorbiscomment',
                    '--append',
                    '--raw',
                    '--commentfile',
                    'pictures.vc',
                    '--',
                    shlex.quote(
                        output_name,
                    ),
                ],
            )

            inputs.append(
                'pictures.vc',
            )

        rule = mustup.core.tup.rule.Rule(
            inputs=inputs,
            command=command,
            outputs=[
                output_name,
            ],
        )

        return rule
