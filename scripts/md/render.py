#!/usr/bin/env python

import codecs
import re
import jinja2
import markdown

def process_slides():
  with codecs.open('../../presentation-output.html', 'w', encoding='utf8') as outfile:
    md = codecs.open('slides.md', encoding='utf8').read()
    md_slides = md.split('\n---\n')
    print 'Compiled %s slides.' % len(md_slides)

    slides = []
    # Process each slide separately.
    for md_slide in md_slides:
      slide = {}
      sections = md_slide.split('\n\n')
      # Extract metadata at the beginning of the slide (look for key: value)
      # pairs.
      metadata_section = sections[0]
      metadata = parse_metadata(metadata_section)
      slide.update(metadata)
      remainder_index = metadata and 1 or 0
      # Get the content from the rest of the slide.
      content_sections = '\n\n'.join(sections[remainder_index:])
      content_sections = content_sections.split('\nslide-notes\n\n')
      content_section = content_sections[0]

      if len(content_sections) > 1:
        note_section = content_sections[1]
        slide['notes'] = markdown.markdown(note_section)

      html = markdown.markdown(content_section, ['attr_list'])
      slide['content'] = postprocess_html(html, metadata)



      slides.append(slide)

    template = jinja2.Template(open('base.html').read())

    outfile.write(template.render(locals()))

def parse_metadata(section):
  """Given the first part of a slide, returns metadata associated with it."""
  metadata = {}
  metadata_lines = section.split('\n')
  for line in metadata_lines:
    colon_index = line.find(':')
    if colon_index != -1:
      key = line[:colon_index].strip()
      val = line[colon_index + 1:].strip()
      metadata[key] = val

  return metadata

def postprocess_html(html, metadata):
  """Returns processed HTML to fit into the slide template format."""
  classString = ""
  if metadata.get('build_lists') and metadata['build_lists'] == 'solid':
    classString = "build"
  if metadata.get('build_lists') and metadata['build_lists'] == 'fade':
    classString = "build fade"
  html = html.replace('<ul>', '<ul class="'+classString+'">')
  html = html.replace('<ol>', '<ol class="'+classString+'">')
  return html

if __name__ == '__main__':
  process_slides()
