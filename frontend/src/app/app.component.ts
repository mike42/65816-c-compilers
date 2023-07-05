import {Component, OnInit} from '@angular/core';
import {CompilerService} from "./compiler.service";

export interface Compiler {
  value: string;
  displayName: string;
  disabled: boolean;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  compilers: Compiler[] = [];
  code = "int sum_numbers_1_to_x(int x) {\n" +
    "    /* Add up all numbers in sequence 1..x */\n" +
    "    int i;\n" +
    "    int sum = 0;\n" +
    "    for(i = 1; i <= x; i++) {\n" +
    "        sum += i;\n" +
    "    }\n" +
    "    return sum;\n" +
    "}"
  result = "; no result available"

  loading = false;
  compilerModel: string = "calypsi-65816";

  constructor(private compilerService: CompilerService) {
  }

  ngOnInit(): void {
    this.compilers = [];
    this.compilerService.listCompilers().subscribe({
      next: (result) => {
        this.compilers = result.map(x => {
          return {value: x.id, displayName: x.name, disabled: !x.available}
        })
      },
      error: (e) => console.error(e)
    });
  }

  doCompile() {
    this.loading = true;
    this.compilerService
      .compile({code: this.code})
      .subscribe({
        next: (result) => {
          this.result = result.asm;
          this.loading = false;
        },
        error: (e) => {
          this.result = "; error";
          this.loading = false;
        }
      });
  }

  public onCodeChange(event: Event) {
    this.code = (event.target as any).value;
  }
}
