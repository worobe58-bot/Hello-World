namespace HelloWorld
{
	// Token: 0x02000003 RID: 3
	public partial class Form1 : global::System.Windows.Forms.Form
	{
		// Token: 0x06000004 RID: 4 RVA: 0x0000207E File Offset: 0x0000027E
		protected override void Dispose(bool disposing)
		{
			if (disposing && this.components != null)
			{
				this.components.Dispose();
			}
			base.Dispose(disposing);
		}

		// Token: 0x06000005 RID: 5 RVA: 0x0000209D File Offset: 0x0000029D
		private void InitializeComponent()
		{
			this.components = new global::System.ComponentModel.Container();
			base.AutoScaleMode = global::System.Windows.Forms.AutoScaleMode.Font;
			base.ClientSize = new global::System.Drawing.Size(800, 450);
			this.Text = "Form1";
		}

		// Token: 0x04000001 RID: 1
		private global::System.ComponentModel.IContainer components;
	}
}
