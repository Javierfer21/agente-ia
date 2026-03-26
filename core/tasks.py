# Este módulo ha sido reemplazado por core/tools.py y core/agents.py
# Se mantiene para compatibilidad con posibles imports externos.

def get_architecture_prompts():
    raise NotImplementedError(
        "get_architecture_prompts() fue eliminado. "
        "Usa core.agents.build_*_agent() y core.tools.* en su lugar."
    )
