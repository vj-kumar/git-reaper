# git-reaper
An useful git assistant

# Config file format

Uses YAML format.
```yaml
<project>:
  url: <downstream url>
  upstream: <upstream url>
  flags: [ force, reverse ]
```

force   - Enables force push  
reverse - Allows to push from downstream to upstream.
