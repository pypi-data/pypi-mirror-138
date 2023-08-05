from pathlib import Path
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Align import MultipleSeqAlignment
import typer
from typing import List, Optional, Tuple

from .xml import BeastXML
from .state import StateTree

app = typer.Typer()


def find_closest_sequence(sequences_from_xml: MultipleSeqAlignment, new_sequence: Seq):
    max_score = None
    seq_id = None
    with typer.progressbar(sequences_from_xml) as progress:
        for i, sequence in enumerate(progress):
            score = sum(
                xi != yi for xi, yi in zip(str(sequence.seq), str(new_sequence))
            )
            if not max_score:
                max_score = score
                seq_id = i
            elif score < max_score:
                max_score = score
                seq_id = i
    if seq_id == "None":
        raise Exception("No Seq found?")
    return seq_id, max_score


def get_sequences_to_add(fasta_file, list_of_seq_ids: list):
    records = SeqIO.parse(fasta_file, "fasta")
    return [record for record in records if record.id not in list_of_seq_ids]


@app.command()
def main(
    xml_file: Path,
    fasta_file: Path,
    state_file: Path = None,
    output: Path = None,
    date_trait: bool = True,
    date_format: str = "%Y-%m-%d",
    date_deliminator: str = "_",
    trait: Optional[List[str]] = typer.Option(
        None,
        help="Trait information 'traitname deliminator group' string seperated by spaces",
    ),
):
    if not state_file:
        state_file = Path(f"{xml_file}.state")
    state_tree = StateTree(state_file)
    traits = [
        {
            "traitname": t.split(" ")[0],
            "deliminator": t.split(" ")[1],
            "group": int(t.split(" ")[2]),
        }
        for t in trait
    ]

    beast_xml = BeastXML(
        xml_file,
        traits,
        date_trait=date_trait,
        date_format=date_format,
        date_deliminator=date_deliminator,
    )

    sequences_to_add = get_sequences_to_add(fasta_file, beast_xml.get_sequence_ids())

    if not sequences_to_add:
        typer.echo("No new sequences found in the fasta file.")
        raise typer.Exit(code=1)

    for sequence in sequences_to_add:
        typer.echo(f"Adding new sequence: {sequence.id}")
        if len(sequence) != beast_xml.alignment.get_alignment_length():
            raise ValueError("Sequences must all be the same length")
        closest_seq_id, max_score = find_closest_sequence(
            beast_xml.alignment, sequence.seq
        )
        new_clade = state_tree.graft(closest_seq_id)
        name = new_clade.name
        new_clade.name = sequence.id
        state_tree.draw()
        new_clade.name = name
        beast_xml.add_sequence(sequence)

    beast_xml.write(out_file=output)
    state_tree.write(out_file=output)
